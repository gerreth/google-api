from googleapiclient.discovery import build
import os
import redis
## Set some global variables
APIKEY = os.environ['APIKEY']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_DB = os.environ['REDIS_DB']
## Initialize redis
r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=REDIS_DB)
'''
Google Cloud Translation API
'''
service = build('translate', 'v2', developerKey=APIKEY)
inputs = ['is it really this easy?', 'amazing technology']
language = 'de'

for sentence in inputs:
    key = 'language_' + language + '_' + sentence
    if r.get(key) == None:
        raw_output = service.translations().list(source='en', target=language, q=sentence).execute()
        output = raw_output['translations'][0]['translatedText']
        r.set(key, output, ex=60*60*24*15)
    else:
        output = r.get(key).decode('utf-8')

    print('translated by Google')
    print('{0} -> {1}'.format(sentence, output))

# # Running Vision API
# import base64
# IMAGE="gs://cloud-training-demos/vision/sign2.jpg"
# vservice = build('vision', 'v1', developerKey=APIKEY)
# request = vservice.images().annotate(body={
#         'requests': [{
#                 'image': {
#                     'source': {
#                         'gcs_image_uri': IMAGE
#                     }
#                 },
#                 'features': [{
#                     'type': 'TEXT_DETECTION',
#                     'maxResults': 3,
#                 }]
#             }],
#         })
# responses = request.execute(num_retries=3)
# print(responses)
#
# foreigntext = responses['responses'][0]['textAnnotations'][0]['description']
# foreignlang = responses['responses'][0]['textAnnotations'][0]['locale']
# print(foreignlang, foreigntext)
#
# inputs=[foreigntext]
# outputs = service.translations().list(source=foreignlang, target='en', q=inputs).execute()
# # print(outputs)
# for input, output in zip(inputs, outputs['translations']):
#   print(u"{0} -> {1}".format(input, output['translatedText']))
#
# lservice = build('language', 'v1beta1', developerKey=APIKEY)
# quotes = [
#   'To succeed, you must have tremendous perseverance, tremendous will.',
#   'It’s not that I’m so smart, it’s just that I stay with problems longer.',
#   'Love is quivering happiness.',
#   'Love is of all passions the strongest, for it attacks simultaneously the head, the heart, and the senses.',
#   'What difference does it make to the dead, the orphans and the homeless, whether the mad destruction is wrought under the name of totalitarianism or in the holy name of liberty or democracy?',
#   'When someone you love dies, and you’re not expecting it, you don’t lose her all at once; you lose her in pieces over a long time — the way the mail stops coming, and her scent fades from the pillows and even from the clothes in her closet and drawers. '
# ]
# for quote in quotes:
#   response = lservice.documents().analyzeSentiment(
#     body={
#       'document': {
#          'type': 'PLAIN_TEXT',
#          'content': quote
#       }
#     }).execute()
#   polarity = response['documentSentiment']['polarity']
#   magnitude = response['documentSentiment']['magnitude']
#   print('POLARITY=%s MAGNITUDE=%s for %s' % (polarity, magnitude, quote))
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
