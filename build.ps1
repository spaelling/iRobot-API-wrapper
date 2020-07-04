docker build -t vacuum .

# list ioamges
docker images
# tag the image we just build
docker tag dd3d20b74f8a dockerbeaver/dockerrepo:vacuum
# push to my own repository
# may need to docker login
docker push dockerbeaver/dockerrepo:vacuum
# can run it like this
docker run -dp 3001:80 --restart always vacuum
# list containers
docker container ls

<# kill a container we dont want
docker container kill inspiring_pike
#>

# can pull and run from repo like this
# sudo docker run -dp 3001:80 --restart always dockerbeaver/dockerrepo:vacuum