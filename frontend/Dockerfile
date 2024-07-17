FROM node:alpine

WORKDIR /app

ADD ./app /app

RUN npm install

RUN npm run build

EXPOSE 3000

# chmod entrypoint and start script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]