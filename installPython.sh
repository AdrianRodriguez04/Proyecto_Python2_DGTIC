#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado. Instalando Python 3..."
    sudo apt update
    sudo apt install -y python3 python3-zip
    echo "Python 3 instalado correctamente."
else
    echo "Python 3 ya está instalado."
fi

echo "Versión de Python instalada:"
python3 --version