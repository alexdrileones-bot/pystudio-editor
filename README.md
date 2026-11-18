# PyStudio — Editor de Imágenes Orientado a Objetos

Aplicación de escritorio desarrollada en Python bajo el paradigma de Programación Orientada a Objetos (POO) que permite cargar imágenes locales, aplicar transformaciones y filtros visuales mediante una interfaz gráfica moderna, gestionar un historial de ediciones y exportar los resultados.

---

## 1. Descripción del problema
Muchas herramientas de edición de imágenes resultan excesivamente complejas para tareas rápidas (como convertir una fotografía a escala de grises, ajustar su contraste, aplicar desenfoque o rotarla), mientras que los scripts de consola carecen de retroalimentación visual inmediata para el usuario. Se requiere una aplicación de escritorio intuitiva, segura frente a errores de formato y diseñada con una arquitectura modular limpia que separe el procesamiento gráfico de la interfaz de usuario.

## 2. Objetivos
* **Objetivo general:** Desarrollar una aplicación de escritorio funcional para la edición básica de imágenes integrando los pilares de la Programación Orientada a Objetos en Python y una interfaz gráfica interactiva.
* **Objetivos específicos:**
  * Aplicar abstracción, herencia y polimorfismo en el diseño de filtros extensibles.
  * Proteger la integridad de la imagen original y el historial de estados mediante encapsulamiento.
  * Implementar una interfaz gráfica en modo oscuro desacoplada de la lógica de negocio.
  * Validar entradas del usuario y manejar excepciones de archivos o parámetros inválidos.

## 3. Funcionalidades
1. **Carga y validación de imágenes:** Permite seleccionar archivos `.png`, `.jpg`, `.jpeg`, `.bmp` y `.webp`, verificando existencia y formato válido.
2. **Aplicación de filtros polimórficos:**
   * *Escala de Grises:* Conversión monocromática preservando canales RGB.
   * *Rotación 90° Horario:* Giro con ajuste automático de dimensiones.
   * *Desenfoque Gaussiano:* Control deslizable de radio (`0.5` a `15.0`).
   * *Ajuste de Contraste:* Control deslizable de intensidad (`0.2` a `3.0`).
3. **Control de historial (Deshacer y Restaurar):** Permite revertir hasta los últimos 10 cambios realizados o volver instantáneamente a la fotografía original.
4. **Exportación de resultados:** Guarda la imagen procesada en el formato y ruta elegidos por el usuario.

## 4. Tecnologías utilizadas
* **Lenguaje:** Python 3.13
* **Interfaz gráfica:** CustomTkinter (`customtkinter`)
* **Procesamiento de imágenes:** Pillow (`PIL`)
* **Pruebas automatizadas:** `unittest` (biblioteca estándar de Python)

## 5. Instalación
1. Clonar este repositorio o descargar el código fuente:
   ```bash
   git clone [https://github.com/TU_USUARIO/pystudio-editor.git](https://github.com/TU_USUARIO/pystudio-editor.git)
   cd pystudio-editor