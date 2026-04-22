FROM python:3.13-bookworm

WORKDIR /MovieAPI

ENV PYTHONPATH=/MovieAPI/app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --dev

COPY app ./app

COPY tests ./tests

RUN chmod +x ./app/prestart.sh

ENTRYPOINT ["./app/prestart.sh"]

CMD ["uv", "run", "pytest"]
