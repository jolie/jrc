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

If the image has been successfully built, then it is possible to compute the 
reconfiguration of a system specified by the \<JSON\> input file (located in 
\<JSONDIR\>) and \<SPEC\> specification file (located in  \<SPECDIR\>) via http
get request at port <PORT>.



```
sudo docker run -i --rm -v <JSONDIR>:/jsondir -v <SPECDIR>:/specdir -t jrc:v1 \
  /jsondir/<JSON> /specdir/<SPEC>
```

Some test examples file can be located in the test subfolder.
Assuming <JSON> is the JSON string containng the current configuration and <SPEC>
is the string containg the specification to obtain the desire configuration it
is possibile to perform the following get requests

http://<IP>:<PORT>/getId?

This will return an <ID> that needs to be used in the following interactions

http://<IP>:<PORT>/sendConf?id=<ID>&conf=<JSON>
http://<IP>:<PORT>/getConf?id=<ID>&spec=<SPEC>

The last get request returns a string containg the JSON representation of the 
desired configuration.

To clean up please lunch the following commands:

```
sudo docker stop jrc_container
sudo docker rm jrc_container
sudo docker rmi jrc
```

For more information, please see the Docker documentation at docs.docker.com




