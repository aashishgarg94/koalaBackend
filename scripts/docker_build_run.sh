./cleanup.sh
docker build -t koala-backend-test .
docker run -d --name koala -p 80:80 -e APP_MODULE="koala.main:app" koala-backend-test