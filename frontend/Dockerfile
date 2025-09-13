# frontend/Dockerfile
FROM node:20-slim

WORKDIR /app

# Copiamos solo package.json para instalar deps una vez
COPY ./package*.json ./

RUN npm ci

# Montaremos el código con volumes desde docker-compose
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
