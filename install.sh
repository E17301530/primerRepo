#!/bin/bash
# -*- ENCODING: UTF-8 -*-
echo "Archivo de instalación de login"
echo "Instalando requerimientos de python"
sudo pip install flask
pip install flask_pymongo
pip install flask_login
pip install werkzeug
pip install bson
echo "requerimientos de python instalados"
echo "Instalación de la base de Datos Mongodb"
sudo apt-get install gnupg
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "Iniciando base de datos"
sudo systemctl start mongod
sudo systemctl enable mongod
echo "Instalación de la base de Datos terminada"
echo "Creación de la base de datos de la aplicacion"
python3 Users.py
echo "Descargando el repositorio de la Aplicacion"
git clone https://github.com/E17301530/primerRepo.git
echo "iniciando la aplicacion"
export FLASK_APP=index.py
python3 index.py
