# TODO: Skip the errors, need to add more stuff here - Uday
docker stop $(docker ps -a -q)

docker rm $(docker ps -a -q)

docker rm $(docker ps -q -f status=exited)

docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
