
FROM lambci/lambda:build-python3.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /var/task

COPY ./Pipfile* ./
RUN pipenv install --dev --keep-outdated

EXPOSE 8000