FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git curl python3 python3-venv python3-pip ffmpeg -y
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm

RUN mkdir /app/
WORKDIR /app/
COPY . /app/

# bikin virtualenv & aktifin
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python3", "-m", "MusicMan"]
