const express = require('express');
const mysql = require('mysql');
const path = require('path');
const app = express();

// Cargar las credenciales desde el archivo .env
const config = require('dotenv').config().parsed;

// Configurar la conexión a la base de datos
const conexion = mysql.createConnection({
  host: config.host,
  user: config.username,
  password: config.password,
  database: config.dbname
});

// Ruta para obtener los datos en formato JSON para Bitcoin
app.get('/datos/bitcoin', (req, res) => {
  obtenerDatosPorMoneda('Bitcoin', res);
});

// Ruta para obtener los datos en formato JSON para Ethereum
app.get('/datos/ethereum', (req, res) => {
  obtenerDatosPorMoneda('Ethereum', res);
});

// Función para obtener datos por moneda desde la base de datos
function obtenerDatosPorMoneda(moneda, res) {
  // Consulta SQL para obtener los registros de la tabla para una moneda específica
  const sql = `SELECT cripto, price, updated FROM criptoinfo WHERE cripto = ?`;

  conexion.query(sql, [moneda], (err, resultados) => {
    if (err) {
      console.error('Error al ejecutar la consulta:', err);
      return res.status(500).json({ error: 'Error al obtener datos' });
    }

    if (resultados.length > 0) {
      const datos = resultados.map(row => ({
        cripto: row.cripto,
        price: row.price,
        updated: row.updated
      }));
      res.json(datos);
    } else {
      res.json([]);
    }
  });
}

// Ruta para servir el archivo HTML
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Iniciar el servidor
const puerto = process.env.PORT || 80;
app.listen(puerto, () => {
  console.log(`Servidor Node.js iniciado en http://localhost:${puerto}`);
});
