# Python 3.12이 설치된 Slim Linux
FROM python:3.12-slim

# 이미지에 메타데이터 추가
LABEL maintainer="sullungim"

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 종속성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libgdbm-dev \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# 사용자 생성
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -

# 환경 변수 설정
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# 의존성 관리 파일 복사
COPY pyproject.toml poetry.lock ./

# 의존성 설치
RUN poetry install --no-root --no-dev

# 나머지 프로젝트 파일 복사
COPY . .

# Django에서 사용할 포트 노출
EXPOSE 8000

# 개발판=True, 배포판=False
ARG DEV=false

# 작업 디렉토리 및 사용자 설정
WORKDIR /app
USER django-user

# 컨테이너 시작 시 실행할 명령어
# CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
