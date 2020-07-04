docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
docker rm $(docker ps -q -f status=exited)
