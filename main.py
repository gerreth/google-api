from googleapiclient.discovery import build
import base64
import json
import os
import redis
## Set some global variables
APIKEY = os.environ['APIKEY']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_DB = os.environ['REDIS_DB']
## Initialize redis
r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=REDIS_DB)
expirationTime = 60*60*24*15
'''
Define function (import later)
'''
def translate(service,sourceLanguage,targetLanguage,inputs):
    for sentence in inputs:
        key = 'translate_' + sourceLanguage + '_' + targetLanguage + '_' + sentence
        if r.get(key) == None:
            raw_output = service.translations().list(source=sourceLanguage, target=targetLanguage, q=sentence).execute()
            output = raw_output['translations'][0]['translatedText']
            r.set(key, output, ex = expirationTime)
        else:
            output = r.get(key).decode('utf-8')

        print('translated by Google')
        print('{0} -> {1}'.format(sentence, output))

def textRecognition(service,service_type,image):
    key = 'vision_' + service_type + '_' + image

    if r.get(key) == None:
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
        r.set(key, json.dumps(responses), ex = expirationTime)
    else:
        responses = json.loads(r.get(key))

    return responses

def languageProcessing(service,service_type,quotes):
    for quote in quotes:
        key = 'language_' + service_type + '_' + quote
        print(key)
        if r.get(key) == None:
            response = service.documents().analyzeSentiment(
                body={
                    'document': {
                    'type': service_type,
                    'content': quote
                }
            }).execute()
            r.set(key, json.dumps(response), ex = expirationTime)
        else:
            response = json.loads(r.get(key))

        polarity = response['documentSentiment']['polarity']
        magnitude = response['documentSentiment']['magnitude']
        print('POLARITY=%s MAGNITUDE=%s for %s' % (polarity, magnitude, quote))

'''
Google Cloud Translation API
'''
service = build('translate', 'v2', developerKey=APIKEY)
inputs = ['is it really this easy?', 'amazing technology']
sourceLanguage = 'en'
targetLanguage = 'de'

translate(service,sourceLanguage,targetLanguage,inputs)
'''
Google Cloud Vision API
'''
service = build('vision', 'v1', developerKey=APIKEY)
image = "gs://cloud-training-demos/vision/sign2.jpg"
service_type = 'TEXT_DETECTION'

responses = textRecognition(service,service_type,image)
## Finally translate text found on image
service = build('translate', 'v2', developerKey=APIKEY)
inputs = [responses['responses'][0]['textAnnotations'][0]['description']]
sourceLanguage = responses['responses'][0]['textAnnotations'][0]['locale']
targetLanguage = 'de'

translate(service,sourceLanguage,targetLanguage,inputs)
'''
Cloud Natural Language API
'''
service = build('language', 'v1beta1', developerKey=APIKEY)
service_type = 'PLAIN_TEXT'
quotes = [
  'To succeed, you must have tremendous perseverance, tremendous will.',
  'It’s not that I’m so smart, it’s just that I stay with problems longer.',
  'Love is quivering happiness.',
  'Love is of all passions the strongest, for it attacks simultaneously the head, the heart, and the senses.',
  'What difference does it make to the dead, the orphans and the homeless, whether the mad destruction is wrought under the name of totalitarianism or in the holy name of liberty or democracy?',
  'When someone you love dies, and you’re not expecting it, you don’t lose her all at once; you lose her in pieces over a long time — the way the mail stops coming, and her scent fades from the pillows and even from the clothes in her closet and drawers. '
]

languageProcessing(service,service_type,quotes)
#
# sservice = build('speech', 'v1beta1', developerKey=APIKEY)
# response = sservice.speech().syncrecognize(
#     body={
#         'config': {
#             'encoding': 'LINEAR16',
#             'sampleRate': 16000
#         },
#         'audio': {
#             'uri': 'gs://cloud-training-demos/vision/audio.raw'
#             }
#         }).execute()
# print(response)
#
# print(response['results'][0]['alternatives'][0]['transcript'])
# print('Confidence=%f' % response['results'][0]['alternatives'][0]['confidence'])
