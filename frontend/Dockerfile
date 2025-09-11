# Usa una imagen base de Node.js
FROM node:20-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos del frontend
COPY ./frontend/ /app/

# Instala las dependencias
RUN npm install

# Compila la aplicación
RUN npm run build

# Expone el puerto para el frontend
EXPOSE 5173

# Ejecuta el servidor de Vue.js
CMD ["npm", "run", "dev"]