FROM python:3.13-bookworm

WORKDIR /mediaservice

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY mediaservice .

COPY packages ./packages

CMD ["uv", "run", "celery", "--app", "core.celery_core.celery_app", "worker", "--loglevel=INFO"]