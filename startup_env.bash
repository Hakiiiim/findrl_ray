#!/bin/bash

# install wrds
pip install wrds

# install swig
pip install swig

# install setuptools
pip install setuptools==65.5.0

# clone the FinRL repository
pip install git+https://github.com/AI4Finance-Foundation/FinRL.git

# install necessary dependencies
sudo apt-get update && sudo apt-get install -y cmake libopenmpi-dev python3-dev zlib1g-dev libgl1-mesa-glx swig

# install gymnasium
pip install gymnasium stockstats dm_tree scikit-image tqdm

#export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
#pip install numpy==1.21
