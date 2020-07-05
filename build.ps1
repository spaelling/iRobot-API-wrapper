$tag = 'vacuum_v1.1'
docker build -t $tag .

# list image
docker images $tag
# tag the image we just build
docker tag d2a214529991 dockerbeaver/dockerrepo:$tag
# push to my own repository
# may need to docker login
docker push dockerbeaver/dockerrepo:$tag

"sudo docker run -dp 3001:80 --restart always dockerbeaver/dockerrepo:$tag" | clip

# can run it like this
docker run -dp 3001:80 --restart always $tag
# list containers
docker container ls

<# kill a container we dont want
docker container kill inspiring_pike
#>

<# can pull and run from repo like this
docker run -dp 3001:80 --restart always dockerbeaver/dockerrepo:vacuum_v2
#>