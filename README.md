# Sistema Asistencia Escuela (Version Beta)
El proyecto es una aplicación de escritorio que gestiona la asistencia de estudiantes y docentes en un colegio, con capacidad para generar códigos de barras, registrar ingresos y generar reportes.
# Lenguaje Principal
Python 3.x (con sintaxis moderna como f-strings)
# Interfaz Gráfica (GUI)
Tkinter - Librería nativa de Python para interfaces gráficas

ttk (Themed Tkinter) - Para widgets con estilos modernos

ttkthemes - Librería que proporciona temas visuales adicionales (plastik)

# Base de Datos

PostgreSQL - Sistema gestor de bases de datos

Psycopg2 - Adaptador PostgreSQL para Python (con soporte para connection pooling)

# Manejo de Imágenes

Pillow (PIL) - Para procesamiento de imágenes (redimensionar/convertir logos)

ImageTk - Integración de imágenes con Tkinter

# Generación de Códigos de Barras

python-barcode - Generación de códigos de barras en formato code128

ImageWriter - Guardado de códigos como imágenes

# Otras Librerías Clave
hashlib - Generación de hashes MD5 para códigos únicos

os - Gestión de variables de entorno (configuración de DB)

datetime - Manejo de fechas y horas

filedialog - Cuadros de diálogo para guardar archivos

# Patrones y Técnicas
Connection Pooling - Gestión eficiente de conexiones a DB

MVC implícito - Separación entre lógica y presentación

Modularización - Organización por funcionalidades (módulos)

Manejo de errores - Bloques try/except para operaciones críticas

Este stack demuestra una arquitectura robusta para aplicaciones de escritorio, combinando eficiencia en el backend (PostgreSQL + pooling) con una interfaz moderna (Tkinter + temas) y funcionalidades especializadas (códigos de barras, reportes multi-formato).

![Screenshot_1](https://github.com/user-attachments/assets/911f3fe0-421b-48df-b43f-9c95d65d79d8)
![Screenshot_2](https://github.com/user-attachments/assets/8e26c865-5165-4833-a633-da9553d981ae)
![Screenshot_3](https://github.com/user-attachments/assets/0716bf5b-96f2-4d52-bb63-f87253f8b428)


