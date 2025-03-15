-------------------------------------------
CREATE DATABASE proyecto;

-------------------------------------------
USE proyecto;

CREATE TABLE mesas (
numero INT PRIMARY KEY,
capacidad INT NOT NULL,
estado ENUM('libre', 'ocupada') DEFAULT 'libre'
);

CREATE TABLE menu (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
descripcion TEXT,
precio DECIMAL(10,2) NOT NULL
);

CREATE TABLE clientes (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
mesaAsignada INT,
FOREIGN KEY (mesaAsignada) REFERENCES mesas(numero)
);

SHOW tables;

EXIT;
