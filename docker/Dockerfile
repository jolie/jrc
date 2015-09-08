FROM python:2-onbuild
MAINTAINER Jacopo Mauro

# install the abs_deployer tool
RUN cd / && \
  git clone https://github.com/jacopoMauro/abs_deployer.git

ENV PATH /abs_deployer:$PATH

# install minizinc suite 1.6 (the 2.0 does not work with zephyrus)
RUN cd / && \
  wget http://www.minizinc.org/downloads/release-1.6/minizinc-1.6-x86_64-unknown-linux-gnu.tar.gz && \
  tar -zxvf minizinc-1.6-x86_64-unknown-linux-gnu.tar.gz && \
  rm -rf minizinc-1.6-x86_64-unknown-linux-gnu.tar.gz && \
  cd /minizinc-1.6 && \
  ./SETUP
ENV PATH /minizinc-1.6/bin:$PATH

# copy zephyrus binaries
COPY ./zephyrus.native /bin/zephyrus.native

WORKDIR /abs_deployer
#ENTRYPOINT ["sunny-cp"]


