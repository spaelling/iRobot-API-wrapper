docker build -t vacuum_v2 .

# list image
docker images vacuum
# tag the image we just build
docker tag c98b4949f62b dockerbeaver/dockerrepo:vacuum_v2
# push to my own repository
# may need to docker login
docker push dockerbeaver/dockerrepo:vacuum_v2
# can run it like this
docker run -dp 3001:80 --restart always vacuum_v2
# list containers
docker container ls

<# kill a container we dont want
docker container kill inspiring_pike
#>

<# can pull and run from repo like this
docker run -dp 3001:80 --restart always dockerbeaver/dockerrepo:vacuum_v2
#>