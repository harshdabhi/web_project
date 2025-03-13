FROM python:3.10-bullseye
COPY . /app
WORKDIR /app 
RUN pip install -r web_django/requirement.txt
# Create a startup script that uses the PORT environment variable
RUN echo '#!/bin/bash\ncd /app/web_django\npython manage.py migrate\npython manage.py create_groups\npython manage.py runserver 0.0.0.0:${PORT:-8000}' > /app/start.sh
RUN chmod +x /app/start.sh
# Expose both the default port and the potential Render port
EXPOSE 8000
CMD ["/app/start.sh"]
