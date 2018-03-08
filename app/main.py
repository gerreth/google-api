import functions.helper as helper
"""
Google Cloud Translation API
"""
inputs = [
    'is it really this easy?',
    'amazing technology',
    'Surprise!'
]
sourceLanguage = 'en'
targetLanguage = 'de'

helper.translate(sourceLanguage,targetLanguage,inputs)
"""
Google Cloud Vision API
"""
image = "gs://cloud-training-demos/vision/sign2.jpg"

service_type = 'TEXT_DETECTION'

responses = helper.textRecognition(service_type,image)
## Finally translate text found on image
inputs = [responses['responses'][0]['textAnnotations'][0]['description']]
sourceLanguage = responses['responses'][0]['textAnnotations'][0]['locale']
targetLanguage = 'de'

helper.translate(sourceLanguage,targetLanguage,inputs)
"""
Cloud Natural Language API
"""
service_type = 'PLAIN_TEXT'
quotes = [
  'The FedEx day will be awesome!',
  'The FedEx day will be great',
  'The FedEx day will be okay',
  'The FedEx day was awesome',
  'The FedEx day was great',
  'The FedEx day will be okay',
  'The FedEx day might be okay',
  'The FedEx day will be bad',
  'The FedEx day will be very bad',
  'The FedEx day was bad',
  'The FedEx day was very bad',
  'The FedEx day is going to be bad',
  'The FedEx day will be awful',
  'The FedEx day was awful',
  'Der FedEx Tag wird großartig!',
  'Der FedEx Tag wird super!',
  'Der FedEx Tag wird gut.',
  'Der FedEx Tag wird okay.',
  'Der FedEx Tag wird nicht so toll!',
  'Der FedEx Tag wird scheisse!',
  'The FedEx day will be awesome! The FedEx day will be great. The FedEx day will be okay',
  'The FedEx day will be awesome! The FedEx day will be great. Der FedEx day wird scheisse',
  'The FedEx day will be awesome! The FedEx day will be not so great. Der FedEx day wird scheisse',
  'The FedEx day will be good! The FedEx day will be not so great. Der FedEx day wird nicht so toll',
  'Kaffee frisch',
]

helper.languageProcessing(service_type,quotes)
"""
Google Cloud Speech API
"""
audio = 'gs://cloud-training-demos/vision/audio.raw'

helper.speechRecognition(audio)
