FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git curl python3 python3-venv python3-pip ffmpeg -y

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm

WORKDIR /app/
COPY . /app/

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python3", "-m", "MusicMan"]
