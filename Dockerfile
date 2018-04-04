FROM guillaumeflorent/miniconda-pythonocc:3-0.18.3

MAINTAINER Guillaume Florent <florentsailing@gmail.com>

RUN conda install -y numpy scipy

RUN conda install -c gflorent corelib

RUN apt-get update && apt-get install -y libgtk2.0-0 && rm -rf /var/lib/apt/lists/*
RUN conda install -y -c anaconda wxpython

RUN conda install -y pyqt
RUN apt-get update && apt-get install -y libgl1-mesa-dev libx11-xcb1 && rm -rf /var/lib/apt/lists/*

# aoc-utils
# TODO : use setup.py
WORKDIR /opt
ADD https://api.github.com/repos/guillaume-florent/aoc-utils/git/refs/heads/master version.json
RUN git clone --depth=1 https://github.com/guillaume-florent/aoc-utils
RUN cp -r /opt/aoc-utils/aocutils /opt/conda/lib/python3.6/site-packages