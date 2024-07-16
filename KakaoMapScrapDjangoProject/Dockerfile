# Python 3.12와 Alpine Linux 3.20을 기반으로 하는 이미지 사용
# docker환경에서 scarp을 하려면 docker에 google chrome을 설치해야 하는데
# 차라리 Python 3.12와 Debian 기반 이미지를 사용하는게 더 쉽다고 한다.
FROM python:3.12-slim

# 이미지의 유지 관리자를 지정
LABEL maintainer="sullungim"

# Python의 표준 입출력 버퍼링을 비활성화하여 로그가 즉시 출력되도록 설정
ENV PYTHONUNBUFFERED=1

# 필요한 파일을 컨테이너로 복사
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
COPY ./.flake8 /app/.flake8

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# 필요한 패키지 설치 및 이미지 최적화
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgbm-dev \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libxshmfence1 \
    libgbm1 \
    xdg-utils \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip setuptools wheel \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && /py/bin/pip install -r /tmp/requirements.dev.txt \
    && rm -rf /tmp

# 환경 변수 설정
ENV PATH="/py/bin:$PATH"
ENV TMPDIR="/tmp"

# 컨테이너가 8000번 포트를 노출하도록 설정 (Django)
EXPOSE 8000

# django-user로 실행
USER root

# Django 프로젝트 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application", "--workers", "4", "--timeout", "120", "--log-level", "debug"]
