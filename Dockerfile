FROM python:3.10-bullseye
COPY . /app
WORKDIR /app 
RUN pip install -r web_django/requirement.txt
EXPOSE 8000
CMD [ "python","./web_django/manage.py","runserver","0.0.0.0:8000" ]
