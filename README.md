# handbrake-webook
A webhook receiver for Sonarr/Radarr that copies files for the handbrake pipeline

## Local setup

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


## Updating PyPi deps

    docker run -it --rm -v ${PWD}:/repo -w /repo python:3.11-slim bash
    pip install --upgrade pip 
    pip install --upgrade pip Flask gunicorn python-consul pulsar-client fastavro pyyaml
    pip freeze > requirements.txt


## Sample Request

Headers:

`Content-Type` `application/json`
`User-Agent` `Radarr/3.2.2.5080 (ubuntu 20.04)`
Request body:

```
{
  "movie":{
    "id":1075,
    "title":"Burn",
    "year":2019,
    "releaseDate":"2019-11-29",
    "folderPath":"/movies/Burn",
    "tmdbId":508138,
    "imdbId":"tt8009314"
  },
  "remoteMovie":{
    "tmdbId":508138,
    "imdbId":"tt8009314",
    "title":"Burn",
    "year":2019
  },
  "movieFile":{
    "id":1371,
    "relativePath":"Burn (2019).mp4",
    "path":"/downloads/Burn (2019) [BluRay] [1080p] [YTS.LT]/Burn.2019.1080p.BluRay.x264-[YTS.LT].mp4",
    "quality":"Bluray-1080p",
    "qualityVersion":1,
    "releaseGroup":"YIFY",
    "sceneName":"Burn.2019.1080p.BluRay.x264-[YTS.LT]",
    "indexerFlags":"G_Freeleech",
    "size":1485653660
  },
  "isUpgrade":false,
  "downloadId":"1748AB53BB522968DC2E400F91EA33FF95CD5F11",
  "eventType":"Download"
}
```
