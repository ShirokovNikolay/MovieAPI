FROM python:3.13-bookworm

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY packages ./packages

COPY app .

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
