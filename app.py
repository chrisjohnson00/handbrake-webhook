from flask import Flask, request
import logging
import os
import consul
import pulsar
from json import dumps
from utilities.skip import skip_send
from api_client.client import SonarrClient, RadarrClient

application = Flask(__name__)
application.logger.setLevel(logging.DEBUG)
required_configs = ['PULSAR_SERVER', 'PULSAR_TOPIC']
CONFIG_PATH = "handbrake-webhook"


@application.route('/')
def index():
    return 'Welcome to the Handbrake Webhook Server!'


@application.route('/webhook', methods=['POST'])
def web_hook():
    application.logger.info("Web hook called")
    application.logger.debug("Web hook headers: {}".format(request.headers))
    application.logger.debug("Web hook data: {}".format(request.get_json()))
    user_agent = request.headers['User-Agent']
    application.logger.info("User-Agent: {}".format(user_agent))
    client = SonarrClient(request.get_json())  # could be any client
    event_type = client.get_event_type()
    # Test is the event type when sonarr sends for a "test" or "save" in settings
    if event_type == "Test":
        return "Test"
    if 'Sonarr' in user_agent:
        client = SonarrClient(request.get_json())
        path = client.get_full_file_path()
        quality = client.get_quality_level()
        if not skip_send(path):
            send_message(path, quality, 'tv')
        else:
            application.logger.info(f"Skipping {path} due to SKIP_CONFIG_FILE match")
    elif 'Radarr' in user_agent:
        client = RadarrClient(request.get_json())
        path = client.get_full_file_path()
        quality = client.get_quality_level()
        send_message(path, quality, 'movie')
    else:
        raise Exception("Boom!  Unexpected user agent: {}".format(user_agent))
    return 'Done'


def send_message(path, quality, type):
    pulsar_server = get_config('PULSAR_SERVER')
    pulsar_topic = get_config('PULSAR_TOPIC')
    application.logger.info("Calculated file path is {}".format(path))
    application.logger.info("Calculated quality level is {}".format(quality))
    if pulsar_server and pulsar_topic:
        client = pulsar.Client(f"pulsar://{pulsar_server}")
        producer = client.create_producer(pulsar_topic)
        message = {'source_full_path': path, 'move_type': 'to_encode', 'type': type, 'quality': quality}
        application.logger.info(f"Sending message {message} to topic '{pulsar_topic}'")
        producer.send(dumps(message).encode('utf-8'))
        application.logger.info(f"Notification sent: message body '{message}', topic '{pulsar_topic}'")
        client.close()
    else:
        application.logger.warning("PULSAR_SERVER or PULSAR_TOPIC was not found in configs, no messages will be sent")


@application.route('/health')
def health_check():
    # client = pulsar.Client(f"pulsar://{get_config('PULSAR_SERVER')}")
    # client.get_topic_partitions(get_config('PULSAR_TOPIC'))
    return "Success"


@application.route('/config')
def config():
    application.logger.info("Rendering config page")
    response_text = ""
    for config in required_configs:
        value = get_config(config)
        if any(secret in config for secret in ['KEY', 'TOKEN', 'PASSWORD']):
            response_text += "{}: [REDACTED]<br/>".format(config)
        else:
            response_text += "{}: {}<br/>".format(config, value)
    return response_text


def get_config(key, config_path=CONFIG_PATH):
    if os.environ.get(key):
        return os.environ.get(key)
    c = consul.Consul()
    index, data = c.kv.get("{}/{}".format(config_path, key))
    return data['Value'].decode("utf-8")


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
