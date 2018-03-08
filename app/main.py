import functions.helper as helper
#import base64
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

helper.translate(sourceLanguage,targetLanguage,inputs)
'''
Google Cloud Vision API
'''
image = "gs://cloud-training-demos/vision/sign2.jpg"
service_type = 'TEXT_DETECTION'

responses = helper.textRecognition(service_type,image)
## Finally translate text found on image
inputs = [responses['responses'][0]['textAnnotations'][0]['description']]
sourceLanguage = responses['responses'][0]['textAnnotations'][0]['locale']
targetLanguage = 'de'

helper.translate(sourceLanguage,targetLanguage,inputs)
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

helper.languageProcessing(service_type,quotes)
'''
Google Cloud Speech API
'''
audio = 'gs://cloud-training-demos/vision/audio.raw'

helper.speechRecognition(audio)
