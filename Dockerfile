FROM python:3.10-slim

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Use dumb-init so the Docker process handles process signals properly
ARG DUMB_INIT_VERSION=1.2.2
RUN python3 -c "\
import urllib.request; \
urllib.request.urlretrieve( \
    'https://github.com/Yelp/dumb-init/releases/download/v${DUMB_INIT_VERSION}/dumb-init_${DUMB_INIT_VERSION}_amd64', \
    '/usr/local/bin/dumb-init' \
) \
" && chmod +x /usr/local/bin/dumb-init

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]

RUN pip install --upgrade pip pipenv && rm -rf ~/.cache

WORKDIR /app

COPY Pipfile* ./
RUN pipenv install --deploy 

COPY . .



EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
