# Completar el Dockerfile para la aplicación frontend
# Usa una imagen base de Node.js para construir la aplicación
FROM node:18 as build

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY package*.json ./
COPY . .

# Instala las dependencias y construye la aplicación
RUN npm install && npm run build

# Usa una imagen base de Nginx para servir los archivos estáticos
FROM nginx:1.23

# Copia los archivos construidos al directorio de Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copia la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto 80
EXPOSE 80

# Comando para ejecutar Nginx
CMD ["nginx", "-g", "daemon off;"]