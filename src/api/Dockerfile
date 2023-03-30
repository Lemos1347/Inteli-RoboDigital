FROM python:3.11.2-alpine3.17

WORKDIR /flask-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3001

COPY . .

ENV MYSQL_MIGRATIONS_HOST='db'
ENV MYSQL_MIGRATIONS_PORT=3306
ENV MYSQL_HOST='db:3306'
ENV MYSQL_DATABASE='DOBOT'
ENV MYSQL_USER='root'
ENV MYSQL_PASSWORD='password12345'


COPY . .

CMD [ "python", "__init__.py" ]