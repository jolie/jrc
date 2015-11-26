# jrc
Jolie Reconfiguration Optimiser

Usage:

```
reconfigurator.py [ <options> ] <json input file> <target specification>
  Options:
    -o, --ofile: file where to save the output
    -d, --dot: dot file where to save the configuration computed by Zephyrus
    -v, --verbose
```

INSTALLATION WITH DOCKER
========================

A simple way to deploy the Jolie Reconfiguration Optimiser is by using Docker 
(www.docker.com). The Dockerfiles needed to generate the container image are 
stored in the docker subfolder. Assuming Docker is installed and \<PATH\> is the 
path to the jrc folder, it is possible to deploy sunny-cp with:

```
sudo docker build -t jrc <PATH>/docker
sudo docker run -d -p <PORT>:9001 --name jrc_container jrc
```

Some test examples file can be located in the test subfolder.
Assuming \<JSON\> is the JSON string containng the current configuration and \<SPEC\>
is the string containg the specification to obtain the desired configuration it
is possibile to perform the following get requests

```
http://<IP>:<PORT>/process?specifications=<JSON>&context==<SPEC>
```

To clean up please lunch the following commands:

```
sudo docker stop jrc_container
sudo docker rm jrc_container
sudo docker rmi jrc
```

For more information, please see the Docker documentation at docs.docker.com




