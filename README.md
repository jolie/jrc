# jrc
Jolie Reconfiguration Optimiser

Usage: reconfigurator.py [<options>] <json input file> <target specification>
  Options:
    -o, --ofile: file where to save the output
    -d, --dot: dot file where to save the configuration computed by Zephyrus
    -v, --verbose

INSTALLATION WITH DOCKER
========================

A simple way to deploy the Jolie Reconfiguration Optimiser is by using Docker
 (www.docker.com).
The Dockerfiles needed to generate the container images are stored in the docker subfolder.

Assuming Docker is installed and <PATH> is the path to the jrc folder, it
is possible to deploy sunny-cp with:

  sudo docker build -t jrc:v1 <PATH>/docker

If the image has been successfully built, then
it is possible to compute the reconfiguration of a system specified by the <JSON> input file
(located in <JSONDIR>) and <SPEC> specification file (located in  <SPECDIR>) invoking the following command:

sudo docker run -i --rm -v <JSONDIR>:/jsondir -v <SPECDIR>:/specdir -t jrc:v1 \
  /jsondir/<JSON> /specdir/<SPEC>

Some test examples file can be located in the test subfolder.
To execute for instance the example test1.json with the specification test1.spec
it is possible to run the following command:

sudo docker run -i --rm -v <JSONDIR>:/jsondir -v <SPECDIR>:/specdir -t jrc:v1 \
  test/test1.json test/test1.spec

For more information, please see the Docker documentation at docs.docker.com

