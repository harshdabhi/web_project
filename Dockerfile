FROM python:3.10-bullseye
COPY . /app
WORKDIR /app 
RUN pip install -r web_django/requirement.txt
CMD [ "python","./web_django/manage.py","runserver" ]
