FROM python:3.8-slim-buster

LABEL maintainer="Tom Ritchford (tom@swirly.com)"
LABEL version="0.7.0"
COPY . .

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "backer"]
CMD []
