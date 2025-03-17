#!/bin/bash

read -s -p "Ingrese una contraseña para MySQL: " contraseniaMySQL
echo ""

if ! command -v mysql &> /dev/null; then
    echo "MySQL no está instalado. Instalando MySQL..."
    sudo apt update
    sudo apt install -y mysql-server
    echo "MySQL instalado correctamente"
else
    echo "MySQL ya esta instalado."
fi

sudo systemctl start mysql

sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${contraseniaMySQL}';"

echo "Creando la base de datos y las tablas..."
sudo mysql -u root -p${contraseniaMySQL} <<EOF
CREATE DATABASE IF NOT EXISTS proyecto;
USE proyecto;

CREATE TABLE IF NOT EXISTS mesas (
numero INT PRIMARY KEY,
capacidad INT NOT NULL,
estado ENUM('libre', 'ocupada') DEFAULT 'libre'
);

CREATE TABLE IF NOT EXISTS clientes (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
mesaAsignada INT,
FOREIGN KEY (mesaAsignada) REFERENCES mesas(numero)
);

CREATE TABLE IF NOT EXISTS menu (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
descripcion TEXT,
precio DECIMAL(10,2) NOT NULL,
activo TINYINT(1) DEFAULT 1
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clienteId INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('preparando','listo','entregado') DEFAULT 'preparando',
    FOREIGN KEY (clienteId) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS detallePedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedidoId INT,
    itemId INT,
    cantidad INT DEFAULT 1,
    FOREIGN KEY (pedidoId) REFERENCES pedidos(id),
    FOREIGN KEY (itemId) REFERENCES menu(id)
);
EOF

echo "Base de datos y tablas creadas correctamente."
echo "Guarde la contraseña de MySQL ('${contraseniaMySQL}') en un lugar seguro."