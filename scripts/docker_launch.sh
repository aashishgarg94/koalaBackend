docker pull udayshankarsingh/koala-backend:born

docker run -d --name koala -p 80:80 -e APP_MODULE="koala.main:app" udayshankarsingh/koala-backend:born