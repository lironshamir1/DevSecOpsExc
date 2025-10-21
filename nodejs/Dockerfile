FROM node:14

ARG API_KEY=hardcoded-api-key-xyz
ARG DB_PASSWORD=password123

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV NODE_ENV=development
ENV API_KEY=$API_KEY
ENV DB_PASSWORD=$DB_PASSWORD
ENV SECRET_KEY=hardcoded-secret-key-12345

RUN chmod 777 /app

EXPOSE 3000

CMD ["node", "server.js"]
