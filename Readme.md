# Project Title

Google API Tests

## Knowledge fundamentals

Intermediate

  * Python

Basic

  * Docker
  * docker-compose
  * redis

## Getting Started

Create a free-trial account on https://cloud.google.com/free/ or use an existing one. **Check current terms and conditions on https://cloud.google.com/free/docs/frequently-asked-questions**

Uses the following APIs

  * [Google Cloud Translation API](https://console.cloud.google.com/apis/library/language.googleapis.com)
  * [Google Cloud Vision API](https://console.cloud.google.com/apis/library/vision.googleapis.com/)
  * [Cloud Natural Language API](https://console.cloud.google.com/apis/library/language.googleapis.com)
  * [Google Cloud Speech API](https://console.cloud.google.com/apis/library/language.googleapis.com)

Activate all of them seperately or give permission to all Google APIs. Go to https://console.cloud.google.com/apis/credentials and create an API KEY. Change
```
API=<YOUR API KEY>
```
in .env-example and rename this file to .env

### Installing

```
docker-compose build
docker-compose up
```
