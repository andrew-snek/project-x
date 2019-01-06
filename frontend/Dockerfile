FROM mhart/alpine-node:11.6

RUN apk add --no-cache bash py-pip && pip install awscli && npm install -g @vue/cli
WORKDIR /vue

EXPOSE 8080