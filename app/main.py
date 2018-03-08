from functions.helper import translate, textRecognition, languageProcessing
import base64
'''
Google Cloud Translation API
'''
inputs = [
    'is it really this easy?',
    'amazing technology',
    'Surprise!'
]
sourceLanguage = 'en'
targetLanguage = 'de'

translate(sourceLanguage,targetLanguage,inputs)
'''
Google Cloud Vision API
'''
image = "gs://cloud-training-demos/vision/sign2.jpg"
service_type = 'TEXT_DETECTION'

responses = textRecognition(service_type,image)
## Finally translate text found on image
inputs = [responses['responses'][0]['textAnnotations'][0]['description']]
sourceLanguage = responses['responses'][0]['textAnnotations'][0]['locale']
targetLanguage = 'de'

translate(sourceLanguage,targetLanguage,inputs)
'''
Cloud Natural Language API
'''
service_type = 'PLAIN_TEXT'
quotes = [
  'To succeed, you must have tremendous perseverance, tremendous will.',
  'It’s not that I’m so smart, it’s just that I stay with problems longer.',
  'Love is quivering happiness.',
  'Love is of all passions the strongest, for it attacks simultaneously the head, the heart, and the senses.',
  'What difference does it make to the dead, the orphans and the homeless, whether the mad destruction is wrought under the name of totalitarianism or in the holy name of liberty or democracy?',
  'When someone you love dies, and you’re not expecting it, you don’t lose her all at once; you lose her in pieces over a long time — the way the mail stops coming, and her scent fades from the pillows and even from the clothes in her closet and drawers. '
]

languageProcessing(service_type,quotes)
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
