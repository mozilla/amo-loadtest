#!/bin/bash
# This is a script to run on a a fresh Ubuntu EC2 instance to get docker
# installed and set up.

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Add the docker sources
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
DOCKER_SRC="deb https://apt.dockerproject.org/repo ubuntu-trusty main"
if grep -Fxq "${DOCKER_SRC}" /etc/apt/sources.list.d/docker.list
then
	echo "docker source already exists"
else
	echo "${DOCKER_SRC}" >> /etc/apt/sources.list.d/docker.list
fi

apt-get update

apt-get install -y linux-image-extra-$(uname -r) docker-engine python-pip
pip install docker-compose
# This is supposed to remove the need for sudo in docker commands but it's not
# working. Hmm.
usermod -a -G docker ubuntu
service docker start

echo
echo "Docker is set up. Next:"
echo "cd ~/amo-loadtest; sudo docker-compose -f ... up -d"
echo "(something like that)"
echo
