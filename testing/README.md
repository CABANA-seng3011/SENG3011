# Unit Tests Microservice
This is a separetly containerised microservice dedicated to running unit & intergration tests on the API and frontend. It will generate a testing report. All tests can be found in `/tests`. Frontend tests were de-prioritised for sprint 2 but will be attended to in sprint 3.

THE TESTS CHECK FOR VALID AND INVALID PARAMETERS, AS WELL AS HANDLING OF SQL EXCEPTIONS
- ALSO CHECK FOR PROPER RESPONSE CODES AND MESSAGES
- USE THE pytest FRAMEWORK AND unittest.mock TO PATCH THE run_sql FUNCTION
- ARE DESIGNED TO BE RUN IN A TESTING ENVIRONMENT
- USE A FIXTURE TO CREATE A TEST CLIENT FOR THE FLASK APP
- USE THE Flask TESTING CONFIGURATION TO ENABLE TESTING MODE
- USE THE app.test_client() METHOD TO CREATE A TEST CLIENT
- USE THE client.get() METHOD TO MAKE GET REQUESTS TO THE /GET ROUTE
- USE THE assert STATEMENT TO CHECK THE RESPONSE STATUS CODE AND DATA
- USE THE mock_run_sql PATCHED FUNCTION TO SIMULATE DATABASE RESPONSES
- USE THE mock_run_sql.side_effect TO SIMULATE EXCEPTIONS
- USE THE mock_run_sql.return_value TO SIMULATE SUCCESSFUL DATABASE RESPONSES

## Unit
These test the functions on their own.

## Integration
These test how the routes interact with the RDS Database.