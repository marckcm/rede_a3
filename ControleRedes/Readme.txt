BIBLIOTECAS:
pip install Flask mysql-connector-python

BANCO DE DADOS:
CREATE DATABASE IF NOT EXISTS rack_management;
USE rack_management;

CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    ip_address VARCHAR(15),
    vlan VARCHAR(50),
    configuration TEXT,
    notes TEXT
);

RODAR APLICAÇÃO:
python app.py
