FROM ubuntu:18.04

WORKDIR /app

ENV PATH=$PATH:/root/.poetry/bin

COPY . .

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get -y --no-install-recommends install \
    curl \
    libcairo-gobject2 \
    libpango1.0-0 \
    python3 \
    python3-distutils \
    python3-pip \
    python3-venv \
 && update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1  \
 && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py > get-poetry.py \
 && python3 get-poetry.py \
 && rm get-poetry.py \
 && pip3 install setuptools \
 && poetry install --no-dev \
 && apt-get -y remove curl python3-pip \
 && apt-get -y autoremove \
 && apt-get clean

EXPOSE 8888

CMD ["poetry", "run", "python3", "main.py"]
