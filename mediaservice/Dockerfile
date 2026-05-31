FROM python:3.13-bookworm

WORKDIR /mediaservice

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY mediaservice .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
