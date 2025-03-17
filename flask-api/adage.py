def getCompany(company_name):
    string = f'Hi {company_name}'
    return string

# {
#     "data_source": "datasource_X",
#     "dataset_type": "sensor_X",
#     "dataset_id": "http://bucket-name.s3-website-Region.amazonaws.com",
#     "time_object": {
#         "timestamp": "2025-03-17 15:01:51.021245",
#         "timezone": "GMT+11"
#     },
#     "events": [
#         {
#             "time_object": {
#                 "timestamp": "2019-07-21 13:04:40.3401012",
#                 "duration": 1,
#                 "duration_unit": "second",
#                 "timezone": "GMT+11"
#             },
#             "event_type": "sensor reading",
#             "attribute": {
#                 "attr1": 36.0,
#                 "attr2": "abc",
#                 "attr3": false
#             }
#         },
#         {
#             "time_object": {
#                 "timestamp": "2019-07-22 13:04:40.301022",
#                 "duration": 1,
#                 "duration_unit": "second",
#                 "timezone": "GMT+11"
#             },
#             "event_type": "sensor reading",
#             "attribute": {
#                 "attr1": 37.0,
#                 "attr2": "bcd",
#                 "attr3": true
#             }
#         }
#     ]
# }