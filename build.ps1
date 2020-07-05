$tag = 'vacuum_v1.2'
docker build -t $tag .

# list image
docker images $tag
# tag the image we just build
docker tag d2a214529991 dockerbeaver/dockerrepo:$tag
# push to my own repository
# may need to docker login
docker push dockerbeaver/dockerrepo:$tag

# paste to dockerhost. kills existing container, prunes stopped containers and runs a new one WARNING: will also prune unrelated containers!
"sudo docker container ps -q --filter name=vacuum | xargs sudo docker container kill`nsudo docker container prune --force`nsudo docker run --name vacuum -dp 3001:80 --restart always dockerbeaver/dockerrepo:$tag`nsudo docker container ps" | clip

# kill container with same name 
"sudo docker container ps -q --filter name=vacuum | xargs sudo docker container kill" | clip
# prune containers
"sudo docker container prune --force" | clip

sudo docker run --name vacuum -dp 3001:80 --restart always dockerbeaver/dockerrepo:vacuum_v1.2

# can run it like this
docker run -dp 3001:80 --restart always $tag
# list containers


<# kill a container we dont want
docker container kill inspiring_pike
#>

<# can pull and run from repo like this
docker run -dp 3001:80 --restart always dockerbeaver/dockerrepo:vacuum_v2
#>