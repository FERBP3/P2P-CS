# Aplicación P2P y cliente-servidor

_Aplicación que utiliza la arquitectura P2P para almacenar en dos nodos los contenidos de un diccionario._
_la aquitectura cliente-servidor para manejar al usuario_

## Comenzando 🚀

### Pre-requisitos 📋

_Se necesita las siguientes herramientas:_
_MariaDB_
_Python3_

### Instalación 🔧

Después de haber instalado MariaDB, ejecutar el archivo mariadb_config/init.sql

_Esto se puede hacer después de haber iniciado sesión_

```
maridb -u $USER -p
source ./mariadb_config/init.sql
```

Luego hay en el archivo p2p/dic_dao.py hay que cambiar el usuario y contraseña por los propios.
Después para ejecutar la aplicación, primero ejecutamos los nodos P2P:
```
python3 p2p/par.py 8000 8080
```
pueden ser con otros puertos siempre y cuando no se utilicen después.

Después ejecutamos el servidor:
```
python3 server-client/server.py 8010 8000 8080
```
Los últimos dos puertos tienen que ser los mismos que los de los nodos P2P para que el servidor
pueda elegir a uno de forma aleatoria. El primer puerto es del servidor y es de libre elección.

Por último ejecutamos el cliente con su interfaz gráfica:
```
python3 server-client/client.py 8010
```
El puerto debe ser el mismo que el del servidor.

