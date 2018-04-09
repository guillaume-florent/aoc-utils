FROM guillaumeflorent/miniconda-pythonocc:3-0.18.3

MAINTAINER Guillaume Florent <florentsailing@gmail.com>

RUN conda install -y numpy scipy pytest
RUN conda install -y -c gflorent corelib aocxchange

RUN apt-get update && apt-get install -y libgtk2.0-0 && rm -rf /var/lib/apt/lists/*
RUN conda install -y -c anaconda wxpython

RUN conda install -y pyqt
RUN apt-get update && apt-get install -y libgl1-mesa-dev libx11-xcb1 && rm -rf /var/lib/apt/lists/*

# aoc-utils
WORKDIR /opt
ADD https://api.github.com/repos/guillaume-florent/aoc-utils/git/refs/heads/master version.json
RUN git clone --depth=1 https://github.com/guillaume-florent/aoc-utils
WORKDIR /opt/aoc-utils
RUN python setup.py install

# Sometimes useful ...
RUN apt-get update && apt-get install -y gedit && rm -rf /var/lib/apt/lists/*