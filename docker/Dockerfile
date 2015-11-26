FROM python:2-onbuild
MAINTAINER Jacopo Mauro

# download the source code
RUN cd / && \
  git clone https://github.com/jolie/jrc.git

ENV PATH /jrc:$PATH

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


# install jolie
RUN apt-get update && \
  apt-get install -y openjdk-7-jdk ant && \
  rm -rf /var/lib/apt/lists/* && \
	cd /  && \
	git clone https://github.com/jolie/jolie.git && \
	cd jolie && \
  ant && ant install

ENV PATH /jrc:$PATH
ENV JOLIE_HOME /usr/lib/jolie

EXPOSE 9001
WORKDIR /jrc
CMD ["jolie", "reconfigurator.ol"]


