# Fun_Api

Hello, welcome to Fun_API.

Fun API allows you access fun contents such as jokes, riddles and African Proverbs.

## Motivation for project

It was built to enable you have fun and also learn. Its a medium through which you can provide interesting content to your end users. Fun API can be integrated in to your application.

## Application build

You can find the source file for the API in this github repo. 

Download the files and run on your development server to understand how the API works

### To start app:

install dependencies in requirements.txt and run app.

```bash
pip install -r requirements.txt
python app.py

```
The api is currently hosted on Heroku and accessed via this URL

```bash
https://fun-apis.herokuapp.com/

```
There are the available endpoints for use.

To access the endpoints one must register as a user for get access token however it is not compulsory for a general user but it is for admin users

- Register for access token

[Get access token - link](https://fun-api.us.auth0.com/authorize?audience=https://localhost:8080&scope=SCOPE&response_type=token&client_id=d22DAcHoKoii94jlf6CZvyIq1ufjyu4F&redirect_uri=https://fun-apis.herokuapp.com&state=STATE)

- Access endpoints through Curl or Postman with access token

1) A general user has permission to access the following endpoints

- get jokes
```bash 
GET https://fun-apis.herokuapp.com/jokes
```
- get riddles
```bash 
GET https://fun-apis.herokuapp.com/riddles
``` 
- post answers to riddles
```bash 
GET https://fun-apis.herokuapp.com/riddle/<id>/answer
```
- get proverbs
```bash 
GET https://fun-apis.herokuapp.com/proverbs
```

2) A admin user has permission to access the following endpoints

- post jokes, riddles and proverbs:
```bash 
POST https://fun-apis.herokuapp.com/jokes
POST https://fun-apis.herokuapp.com/riddles
POST https://fun-apis.herokuapp.com/proverbs
```

- update jokes, riddles and proverbs

```bash
PATCH https://fun-apis.herokuapp.com/jokes/<id>
PATCH https://fun-apis.herokuapp.com/riddles/<id>
PATCH https://fun-apis.herokuapp.com/proverbs/<id>
```

- delete jokes, riddles and proverbs

```bash
DELETE https://fun-apis.herokuapp.com/jokes/<id>
DELETE https://fun-apis.herokuapp.com/riddles/<id>
DELETE https://fun-apis.herokuapp.com/proverbs/<id>
```


