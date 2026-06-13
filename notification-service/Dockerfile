FROM python:3.13-bookworm

WORKDIR /notification-service

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY packages ./packages

COPY notification-service .

CMD ["uv", "run", "python", "main.py"]