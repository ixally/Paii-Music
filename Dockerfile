FROM debian:latest

# Update & install dependencies dasar
RUN apt update && apt upgrade -y && \
    apt install -y \
    git \
    curl \
    python3 \
    python3-venv \
    python3-pip \
    ffmpeg \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 18 & npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm i -g npm && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy semua file
COPY . /app/

# Setup virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip dan install dependencies Python
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Jalankan bot
CMD ["python3", "-m", "MusicMan"]
