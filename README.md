# **PROYECTO PYTHON - DGTIC**
## **SISTEMA DE UN RESTAURANTE**
**Realizado por:**
- **Adrián Leonardo Rodríguez Pichardo**

## **Introducción** 
Este repositorio personal sirve para guardar mi Proyecto de Python
en el cual se tiene como proposito brindar un sistema de pedidos para 
clientes de un restaurante y de igual forma que el administrador
gestione dicho restaurante desde este sistema. Se creó una base de 
datos en MySQL para que toda la información se guarde en dicha BD.

## **Requisitos**
- Sistema operativo GNU/Liux compatible.
- Conexión a internet para descargar los archivos

## **¿Qué documentos encontraremos en este repositorio?**
- README: Presentación del proyecto.
- proyecto.py: Programa principal del proyecto.
- requirements.txt: Paquetería necesaria para la ejecución del programa.
- installPython.sh: Script para descargar Python
- setupBd.sh: Script que descargar MySQL y al mismo tiempo crea la BD.
- base.sql: Base de datos por si se dea modificar o visualizar contenido.

## **Pasos para poder hacer funcionar el proyecto en una terminal**
1. Lo primero que tenemos que hacer es descargar todos los archivos que se encuentran en este repositorio.
2. Tenemos que darle permisos de ejecución a ambos scripts de la siguiente manera:
    - *chmod +x installPython.sh*
    - *chmod +x setupBD.sh*
3. Ejecutaremos el script **installPython.sh** de la siguiente manera:
    - *./installPython.sh*
4. Seguido a esto es necesario instalar las dependecias del proyecto usando pip de la siguiente manera:
    - *pip install -r requirements.txt*
5. Ejecutamos el segundo script **setupBD.sh** de la siguiente manera (NOTA: Es importante saber que durante la ejecución del script se solicitará una contraseña para MySQL la cual es vital guardar muy bien puesto que servirá para futuras conexiones):
    - *./setupBD.sh*
6. Por último, teniendo las configuraciones anteriores, ahora sí podemos ejecutar el programa con el siguiente comando:
    - *python3 proyecto.py*

## **Notas finales**
- El código cuenta con varios comentarios para que sea más entendible lo que hace cada cosa.
- Este repositorio cuenta con varios commits que registran la vida del proyecto a lo largo de este periodo de tiempo, en donde se muestra todos los cambios realizados desde el primer momento.

