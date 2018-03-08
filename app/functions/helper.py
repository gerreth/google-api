from googleapiclient.discovery import build
import json
import math
import os
import redis
## Set some global variables
APIKEY = os.environ['APIKEY']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_DB = os.environ['REDIS_DB']
REDIS_ANALYZE = os.environ['REDIS_ANALYZE']
"""
Helper classes
"""
class RedisCache():
    """
    Currently set to 15 days.
    To-do: Check if this is appropriate
    """
    expirationTime = 60*60*24*15

    def __init__(self):
        self.r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=REDIS_DB)
    def get(self,key):
        if self.r.get(key) != None:
            return json.loads(self.r.get(key))
        return None
    def set(self,key,value):
        self.r.set(key, json.dumps(value), ex = self.expirationTime)

class RedisGoogleLimitTracker():
    """
    Google Cloud Translation API:   ... To-do ...
    Google Cloud Vision API:        ... To-do ...
    Cloud Natural Language API:     Check limits and unitlength on https://cloud.google.com/natural-language/pricing
    Google Cloud Speech API:        ... To-do ...
    """
    track = {
        'translate': {},
        'vision': {},
        'language': {
            'limit': 5000
            'unitlength': 1000
        },
        'speech': {}
    }
    """
    To-do: calculate seconds to end of month
    """
    expirationTime = 60*60*24*31

    def __init__(self):
        self.r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=REDIS_ANALYZE)
    def incrby(self,key,value):
        by = math.ceil(len(value)/self.track[key].unitlength)
        if self.r.get(key) == None:
            self.r.set(key, by, ex = self.expirationTime)
        else:
            self.r.incrby(key, by)

RedisCache = RedisCache()
RedisGoogleLimitTracker = RedisGoogleLimitTracker()
"""
Helper functions
"""
def translate(sourceLanguage,targetLanguage,inputs):
    """
    Args:
        sourceLanguage (str): language of input sentence
        targetLanguage (str): language of output sentence
        inputs (list of str): List of sentences to translate
    """
    service = build('translate', 'v2', developerKey=APIKEY)
    for sentence in inputs:
        key = 'translate_' + sourceLanguage + '_' + targetLanguage + '_' + sentence
        output = RedisCache.get(key)
        if output == None:
            raw_output = service.translations().list(source=sourceLanguage, target=targetLanguage, q=sentence).execute()
            output = raw_output['translations'][0]['translatedText']
            RedisCache.set(key,output)

        print('{0} -> {1}'.format(sentence, output))

def textRecognition(service_type,image):
    """
    Args:
        service_type (str): 'TEXT_DETECTION', ...
        audio (str): url of image stored in Google Cloud Storage
    """
    service = build('vision', 'v1', developerKey=APIKEY)
    key = 'vision_' + service_type + '_' + image
    responses = RedisCache.get(key)
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
        RedisCache.set(key,responses)

    return responses

def languageProcessing(service_type,quotes):
    """
    Args:
        service_type (str): 'PLAIN_TEXT', ...
        quotes (list of str): List of sentences to analyze
    """
    service = build('language', 'v1beta1', developerKey=APIKEY)
    for quote in quotes:
        key = 'language_' + service_type + '_' + quote
        response = RedisCache.get(key)
        if response == None:
            response = service.documents().analyzeSentiment(
                body={
                    'document': {
                    'type': service_type,
                    'content': quote
                }
            }).execute()

            RedisCache.set(key,response)
            RedisGoogleLimitTracker.incrby('language',quote)

        polarity = response['documentSentiment']['polarity']
        magnitude = response['documentSentiment']['magnitude']
        print('POLARITY=%s MAGNITUDE=%s for %s' % (polarity, magnitude, quote))

def speechRecognition(audio):
    """
    Args:
        audio (str): url of .wav audio clip
    """
    service = build('speech', 'v1beta1', developerKey=APIKEY)
    key = 'speech_' + audio
    response = RedisCache.get(key)
    if response == None:
        response = service.speech().syncrecognize(
            body={
                'config': {
                    'encoding': 'LINEAR16',
                    'sampleRate': 16000
                },
                'audio': {
                    'uri': audio
                    }
                }).execute()

    print(response['results'][0]['alternatives'][0]['transcript'])
    print('Confidence=%f' % response['results'][0]['alternatives'][0]['confidence'])
