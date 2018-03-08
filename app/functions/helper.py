from googleapiclient.discovery import build
import json
import os
import redis
## Set some global variables
APIKEY = os.environ['APIKEY']
'''
Helper class
'''
class RedisHelper():
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_DB = os.environ['REDIS_DB']
    expirationTime = 60*60*24*15

    def __init__(self):
        self.r = redis.StrictRedis(host=self.REDIS_HOST, port=6379, db=self.REDIS_DB)
    def get(self,key):
        return json.loads(self.r.get(key))
    def set(self,key,value):
        self.r.set(key, json.dumps(value), ex = self.expirationTime)

rh = RedisHelper()
'''
Helper functions
'''
def translate(sourceLanguage,targetLanguage,inputs):
    service = build('translate', 'v2', developerKey=APIKEY)
    for sentence in inputs:
        key = 'translate_' + sourceLanguage + '_' + targetLanguage + '_' + sentence
        output = rh.get(key)
        if output == None:
            raw_output = service.translations().list(source=sourceLanguage, target=targetLanguage, q=sentence).execute()
            output = raw_output['translations'][0]['translatedText']
            rh.set(key,output)

        print('{0} -> {1}'.format(sentence, output))

def textRecognition(service_type,image):
    service = build('vision', 'v1', developerKey=APIKEY)
    key = 'vision_' + service_type + '_' + image
    responses = rh.get(key)
    if responses == None:
        request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'source': {
                        'gcs_image_uri': image
                    }
                },
                'features': [{
                    'type': service_type,
                    'maxResults': 3,
                }]
            }],
        })
        responses = request.execute(num_retries=3)
        rh.set(key,responses)

    return responses

def languageProcessing(service_type,quotes):
    service = build('language', 'v1beta1', developerKey=APIKEY)
    for quote in quotes:
        key = 'language_' + service_type + '_' + quote
        response = rh.get(key)
        if response == None:
            response = service.documents().analyzeSentiment(
                body={
                    'document': {
                    'type': service_type,
                    'content': quote
                }
            }).execute()
            rh.set(key,response)

        polarity = response['documentSentiment']['polarity']
        magnitude = response['documentSentiment']['magnitude']
        print('POLARITY=%s MAGNITUDE=%s for %s' % (polarity, magnitude, quote))
