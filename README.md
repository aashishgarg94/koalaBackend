### OAuth vs JWT

https://stackoverflow.com/questions/25611167/do-i-need-oauth2-for-my-web-apps-api

- [Black](https://github.com/psf/black)
- [Black Blog](https://www.freecodecamp.org/news/auto-format-your-python-code-with-black/)

#### Black Dev
```pipenv install black --dev --pre)```

#### Lint Usage
```black ./koala```

#### [globbing install](https://stackoverflow.com/questions/30539798/zsh-no-matches-found-requestssecurity)
```use quotes while instlal glob```

#### [mongo On Local](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

#### [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac/)

#### Check port
```sudo lsof -iTCP -sTCP:LISTEN | grep mongo```


#### Running on local
```shell script
uvicorn koala.main:app --reload
```

### New Flow
1. Production - SNS -> SQS -> HTTP Server(EB) -> all background work will happen here
2. Development - SNS -> SQS = Implemented (Periodic pull can be done)(Postman can be use for pull and verifying data)

###
- koala
|--modules
  |--app_module


### Logic for data in, processing and out
1. Pydantic(fastapi)


### Important Links
 - 