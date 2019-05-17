import googleapiclient.discovery

instances = [['F', '0-17', 10, 'A', '2', 0, 1, 6.0, 14.0,
        15200],
       ['M', '46-50', 7, 'B', '2', 1, 1, 8.0, 17.0,
        19215],
             ]


PROJECT_ID = "artefact-ml-specialization"
MODEL_NAME = "blackfriday"
VERSION_NAME = "v21"
service = googleapiclient.discovery.build('ml', 'v1')
name = 'projects/{}/models/{}/versions/{}'.format(PROJECT_ID, MODEL_NAME, VERSION_NAME)

response = service.projects().predict(
    name=name,
    body={'instances': instances}
).execute()

if 'error' in response:
    raise RuntimeError(response['error'])
else:
  print(response['predictions'])


# response = service.projects().predict(
#     name=name,
#     body={'instances': instances, 'probabilities': True}
# ).execute()
#
# if 'error' in response:
#     raise RuntimeError(response['error'])
# else:
#   print(response['predictions'])