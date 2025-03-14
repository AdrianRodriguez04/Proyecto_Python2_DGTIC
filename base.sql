**-------------------------------------------
CREATE DATABASE restaurante;

CREATE USER 'empleado'@'localhost' IDENTIFIED BY 'contraseñaPropia';

GRANT ALL PRIVILEGES ON restaurante.* TO 'empleado'@'localhost';
FLUSH PRIVILEGES;

EXIT;

**-------------------------------------------
USE restaurante;

CREATE TABLE mesas (
id INT AUTO_INCREMENT PRIMARY KEY,
numero INT NOT NULL,
capacidad INT NOT NULL,
estado VARCHAR(20) DEFAULT 'libre'
);

CREATE TABLE menu(
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
descripcion TEXT,
precio DECIMAL(10,2) NOT NULL
);

CREATE TABLE clientes(
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
mesaAsignada INT,
FOREIGN KEY (mesaAsignada) REFERENCES mesas(id)
);

CREATE TABLE pedidos (
id INT AUTO_INCREMENT PRIMARY KEY,
clienteId INT,
estado VARCHAR(20) DEFAULT 'preparando',
FOREIGN KEY (clienteId) REFERENCES clientes(id)
);

CREATE TABLE itemsPedido(
id INT AUTO_INCREMENT PRIMARY KEY,
pedidoId INT,
itemId INT,
FOREIGN KEY (pedidoId) REFERENCES pedidos(id),
FOREIGN KEY (itemId) REFERENCES menu(id)
);

SHOW tables;

EXIT;







