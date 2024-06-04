FROM python:3.11-slim-bullseye as requirements

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

WORKDIR ${APP_HOME}

COPY --from=requirements /tmp/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--port", "8080"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
