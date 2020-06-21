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

## Endpoint authentication and use
There are the available endpoints for use.

To access the endpoints one must register as a user for get access token for authentication

- Register for access token

[login & get access token - link](https://fun-api.us.auth0.com/authorize?audience=https://localhost:8080&scope=SCOPE&response_type=token&client_id=d22DAcHoKoii94jlf6CZvyIq1ufjyu4F&redirect_uri=https://fun-apis.herokuapp.com&state=STATE)

```bash
NB
Temporary user accounts with general and admin privileges have been created to login to test the endpoints. Check file "Test_credentials" in this github repo or you can choose to sign up.
Alternatively there are temporary bearer token in "testconfig.py" in the repo
```

- Access endpoints through Curl or Postman with access token

1) A general user has permission to access the following endpoints

- get jokes
	* Reload to see new joke
```bash
GET https://fun-apis.herokuapp.com/jokes
curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://fun-apis.herokuapp.com/jokes
```
- get riddle
	* Reload to see new riddle
```bash
GET https://fun-apis.herokuapp.com/riddle
curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://fun-apis.herokuapp.com/riddle
```
- post answer to riddle
	* attach answer to a json file. {"answer": XXX}
```bash
POST https://fun-apis.herokuapp.com/riddle/<id>/answer
ex.
curl -X POST -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/JSON" -d '{ "answer":"fingers"}' https://fun-apis.herokuapp.com/riddle/4/answer

```
- get proverbs
	* Reload to see new proverb
```bash
GET https://fun-apis.herokuapp.com/proverbs
curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://fun-apis.herokuapp.com/proverbs
```

2) A admin user has permission to access the following endpoints, including permissions of a general user

- post jokes, riddle and proverbs - attach joke, riddle or proverbs to a json file
```bash
POST https://fun-apis.herokuapp.com/jokes
POST https://fun-apis.herokuapp.com/riddle
POST https://fun-apis.herokuapp.com/proverbs
```

- update jokes, riddle and proverbs - attach joke, riddle or proverbs to update to a json file

```bash
PATCH https://fun-apis.herokuapp.com/jokes/<id>
PATCH https://fun-apis.herokuapp.com/riddle/<id>
PATCH https://fun-apis.herokuapp.com/proverbs/<id>
```

- delete jokes, riddle and proverbs

```bash
DELETE https://fun-apis.herokuapp.com/jokes/<id>
DELETE https://fun-apis.herokuapp.com/riddle/<id>
DELETE https://fun-apis.herokuapp.com/proverbs/<id>
```


