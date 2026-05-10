FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml ./
COPY src ./src
COPY tests ./tests

RUN uv pip install --system -e .

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.tgz \
    && tar -xzf allure-2.29.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.29.0/bin/allure /usr/local/bin/allure \
    && rm allure-2.29.0.tgz

CMD ["pytest", "--alluredir=allure-results"]
