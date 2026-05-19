FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY backend ./backend

RUN uv pip install --system -e .

CMD ["uv", "run", "pytest", "backend/tests", "--alluredir=allure-results"]
