FROM node:18-alpine
WORKDIR /app
COPY package.json package.json
COPY webpack.config.js webpack.config.js
COPY public public
COPY src src
RUN npm install --legacy-peer-deps
EXPOSE 3000
CMD ["npm", "start"]