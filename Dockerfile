# Usa una imagen base de Node.js
FROM node

# Establece el directorio de trabajo en la aplicación
WORKDIR /usr/src/app

# Copia el archivo package.json e instala las dependencias
COPY package*.json ./
RUN npm install

# Copia los archivos de la aplicación
COPY . .

# Expone el puerto 3000
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["node", "server.js"]
