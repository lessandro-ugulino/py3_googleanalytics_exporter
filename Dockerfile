FROM python:3
LABEL Maintainer="lessandro.ugulino@gmail.com"

RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir google-oauth2-tool
RUN pip install --no-cache-dir google-api-python-client
RUN pip install --no-cache-dir prometheus_client

VOLUME  ["/app"]
ADD main.py /

CMD [ "python", "/main.py" ]