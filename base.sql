-------------------------------------------
CREATE DATABASE proyecto;

-------------------------------------------
USE proyecto;

CREATE TABLE mesas (
numero INT PRIMARY KEY,
capacidad INT NOT NULL,
estado ENUM('libre', 'ocupada') DEFAULT 'libre'
);

CREATE TABLE clientes (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
mesaAsignada INT,
FOREIGN KEY (mesaAsignada) REFERENCES mesas(numero)
);

CREATE TABLE menu (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
descripcion TEXT,
precio DECIMAL(10,2) NOT NULL
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clienteId INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('preparando','listo','entregado') DEFAULT 'preparando',
    FOREIGN KEY (clienteId) REFERENCES clientes(id)
);

CREATE TABLE detallePedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedidoId INT,
    itemId INT,
    cantidad INT DEFAULT 1,
    FOREIGN KEY (pedidoId) REFERENCES pedidos(id),
    FOREIGN KEY (itemId) REFERENCES menu(id)
);

SHOW tables;

EXIT;
