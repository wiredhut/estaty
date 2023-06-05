FROM python:3.10
RUN pip install "poetry==1.3.2"

# Copy code
WORKDIR /code

# Install dependencies
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "estaty" == production && echo "--no-dev") --no-interaction --no-ansi

# Copy necessary code
COPY ./app /code/app
COPY ./estaty /code/estaty

# Socket configuration
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]