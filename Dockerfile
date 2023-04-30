FROM rayproject/ray-ml:latest

#RUN apk update && apk add python3-dev \
#                          gcc \
#                          libc-dev \
#                          libffi-dev

# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt update && apt install libosmesa6-dev libgl1-mesa-glx libglfw3 patchelf

COPY requirements.txt /tmp/
COPY FinRL /tmp/

RUN pip install --requirement /tmp/requirements.txt
RUN pip install jupyterlab

COPY . /findrl/
WORKDIR /findrl

RUN pip install -e /findrl/FinRL/.