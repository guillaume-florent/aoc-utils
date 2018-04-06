FROM guillaumeflorent/miniconda-pythonocc:3-0.18.3

MAINTAINER Guillaume Florent <florentsailing@gmail.com>

RUN conda install -y numpy scipy pytest

RUN conda install -c gflorent corelib aocxchange

RUN apt-get update && apt-get install -y libgtk2.0-0 && rm -rf /var/lib/apt/lists/*
RUN conda install -y -c anaconda wxpython

RUN conda install -y pyqt
RUN apt-get update && apt-get install -y libgl1-mesa-dev libx11-xcb1 && rm -rf /var/lib/apt/lists/*

# aocxchange
## TODO : use setup.py or conda package
WORKDIR /opt
#ADD https://api.github.com/repos/guillaume-florent/aoc-xchange/git/refs/heads/master version.json
#RUN git clone --depth=1 https://github.com/guillaume-florent/aoc-xchange
#RUN cp -r /opt/aoc-xchange/aocxchange /opt/conda/lib/python3.6/site-packages

# aoc-utils
## TODO : use setup.py
ADD https://api.github.com/repos/guillaume-florent/aoc-utils/git/refs/heads/master version.json
RUN git clone --depth=1 https://github.com/guillaume-florent/aoc-utils
#RUN cp -r /opt/aoc-utils/aocutils /opt/conda/lib/python3.6/site-packages

WORKDIR /opt/aoc-utils
RUN python setup.py install