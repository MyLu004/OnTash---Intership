# frontend/Dockerfile
FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Use nginx to serve it
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
