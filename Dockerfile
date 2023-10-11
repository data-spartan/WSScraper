FROM python:3.8

ADD utils utils/
ADD main.py .
COPY .env.production .env
COPY constants.py .
COPY requirements.txt .
ADD sender.py .
COPY docker-entrypoint.sh .
RUN pip install -r requirements.txt
CMD ["bash", "docker-entrypoint.sh"]

