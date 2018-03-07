APIKEY="AIzaSyDRxkhVR4xPnuVqsKfNlkWpU5Wuqii0c54"

# running Translate API
from googleapiclient.discovery import build
service = build('translate', 'v2', developerKey=APIKEY)

# use the service
inputs = ['is it really this easy?', 'amazing technology', 'Cloud Dataprep is Googles self-service data preparation tool built in collaboration with Trifacta. In this lab you will learn how to clean and enrich multiple datasets using Cloud Dataprep. The lab exercises are based on a mock use case scenario.']
outputs = service.translations().list(source='en', target='de', q=inputs).execute()
# print outputs
for input, output in zip(inputs, outputs['translations']):
  print(u"{0} -> {1}".format(input, output['translatedText'].encode('ascii', 'ignore').decode('ascii')))
  print(" ")
