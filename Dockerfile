FROM jammy-22.04
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
CMD [ "python","./web_django/manage.py","runserver" ]
