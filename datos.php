<?php
error_reporting(E_ALL);

// Leer las credenciales desde el archivo de configuración
$config = parse_ini_file('config.ini');

// Conexión a la base de datos
$conexion = new mysqli($config['host'], $config['username'], $config['password'], $config['dbname']);

// Verificar la conexión
if ($conexion->connect_error) {
    die("Error de conexión a la base de datos: " . $conexion->connect_error);
}

// Consulta SQL para obtener el último registro de la tabla
$sql = "SELECT latitude, longitude, time_stamp FROM ubication ORDER BY time_stamp DESC LIMIT 30";

$resultado = $conexion->query($sql);

if ($resultado->num_rows > 0) {
    $fila = $resultado->fetch_assoc();
    
    // Convertir los datos en un arreglo asociativo
    $datos = array(
        "latitude" => $fila["latitude"],
        "longitude" => $fila["longitude"],
        "time_stamp" => $fila["time_stamp"]
    );
    echo json_encode($datos);
} else {
    echo "No se encontraron datos en la tabla.";
}

// Cerrar la conexión a la base de datos
$conexion->close();
?>
