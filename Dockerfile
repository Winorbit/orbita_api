FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /home/web_api/

COPY Pipfile* /home/web_api/

RUN pip install --no-cache-dir pipenv && pipenv install --deploy --system

COPY . /home/web_api/

RUN chmod +x /home/web_api/entrypoint.sh

ENTRYPOINT [ "/home/web_api/entrypoint.sh" ]
