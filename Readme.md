# Project Title

Google API Tests

## Introduction

Uses the following APIs:

  * [Google Cloud Translation API](https://console.cloud.google.com/apis/library/language.googleapis.com)
  * [Google Cloud Vision API](https://console.cloud.google.com/apis/library/vision.googleapis.com/)
  * [Cloud Natural Language API](https://console.cloud.google.com/apis/library/language.googleapis.com)
  * [Google Cloud Speech API](https://console.cloud.google.com/apis/library/language.googleapis.com)

## Getting Started

Go to https://console.cloud.google.com/apis/credentials and create an API KEY. Change
```
API=<YOUR API KEY>
```
in .env-example and rename this file to .env

### Installing

```
docker-compose build
docker-compose up
```
