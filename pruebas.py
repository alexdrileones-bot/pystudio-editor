import os
import tempfile
import unittest
from PIL import Image

from modelos import (
    FiltroEscalaGrises,
    FiltroDesenfoque,
    FiltroContraste,
    FiltroRotacion,
)
from servicios import EditorServicio


class TestEditorImagenes(unittest.TestCase):
    """Pruebas unitarias para validar la lógica POO y el manejo de errores."""

    def setUp(self) -> None:
        self.archivo_temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img = Image.new("RGB", (100, 80), color=(120, 180, 240))
        img.save(self.archivo_temp.name)
        self.archivo_temp.close()

        self.servicio = EditorServicio()

    def tearDown(self) -> None:
        if os.path.exists(self.archivo_temp.name):
            os.remove(self.archivo_temp.name)

    def test_carga_y_rotacion_polimorfica(self) -> None:
        proyecto = self.servicio.cargar_imagen(self.archivo_temp.name)
        self.assertEqual(proyecto.dimensiones, (100, 80))

        img_rotada = self.servicio.aplicar_filtro(FiltroRotacion(90))
        self.assertEqual(img_rotada.size, (80, 100))
        self.assertTrue(proyecto.puede_deshacer)

    def test_historial_deshacer_y_restaurar(self) -> None:
        self.servicio.cargar_imagen(self.archivo_temp.name)
        self.servicio.aplicar_filtro(FiltroEscalaGrises())
        self.servicio.aplicar_filtro(FiltroContraste(1.5))

        self.assertTrue(self.servicio.deshacer_cambio())
        self.servicio.restaurar_original()
        self.assertFalse(self.servicio.proyecto_actual.puede_deshacer)

    def test_error_formato_invalido(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as txt_temp:
            txt_temp.write(b"no es una imagen")
            ruta_txt = txt_temp.name

        try:
            with self.assertRaises(ValueError):
                self.servicio.cargar_imagen(ruta_txt)
        finally:
            os.remove(ruta_txt)

    def test_error_parametro_filtro_fuera_de_rango(self) -> None:
        with self.assertRaises(ValueError):
            FiltroDesenfoque(radio=-5.0)


if __name__ == "__main__":
    unittest.main()