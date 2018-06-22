# Base OS:
FROM ubuntu

# setting up OS:
RUN echo                                                \
  && apt-get update                                     \
  && apt-get install -y apt-utils                       \
  && apt-get install -y software-properties-common      \
  && apt-get install -y build-essential                 \
  && apt-get install -y dumb-init
  # dumb-init for writing easy entrypoints


# Setting up java:
RUN echo                                                \
  && apt-get install -y default-jdk                     \
  && apt-get install -y default-jre


# Setting up the python:
RUN echo                                                \
  && apt-get install -y python3-pip                     \
  && pip3 install -U setuptools


# Setting up the requirements:
RUN echo                                                \
  && pip3 install numpy                                 \
  && pip3 install -U python-telegram-bot                \
  && pip3 install -U wolframalpha                       \
  && pip3 install -U pycorenlp                          \
  && pip3 install -U yandex.translate                   \
  && pip3 install -U gensim                             \
  && pip3 install -U pyemd                              \
  && pip3 install -U pandas


# Copying all files from current directory to container for further execution:
COPY . /

# For testing
ENTRYPOINT ["/bin/bash"]