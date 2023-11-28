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

// Consulta SQL para obtener los registros de la tabla
$sql = "SELECT cripto, price, datetime FROM criptoinfo ;

$resultado = $conexion->query($sql);

if ($resultado->num_rows > 0) {
    $fila = $resultado->fetch_assoc();
    
    // Convertir los datos en un arreglo asociativo
    $datos = array(
        "cripto" => $fila["cripto"],
        "price" => $fila["price"],
        "updated" => $fila["datetime"]
    );
    echo json_encode($datos);
} else {
    echo "No se encontraron datos en la tabla.";
}

// Cerrar la conexión a la base de datos
$conexion->close();
?>
