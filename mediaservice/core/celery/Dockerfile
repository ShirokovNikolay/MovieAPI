FROM python:3.13-bookworm

WORKDIR /celery-worker

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY mediaservice/core/celery .

CMD ["uv", "run", "celery", "--app", "celery_app", "worker", "--loglevel=INFO"]