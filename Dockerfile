FROM alpine:latest

RUN apk add --no-cache py3-pip bash
 
RUN python3 -m pip install scrapy
 
WORKDIR /app

# docker build -t tapuz .
# docker run -it --mount type=bind,source="${PWD}",target=/app tapuz /bin/bash