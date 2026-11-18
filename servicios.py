from typing import Optional
from PIL import Image
from modelos import ImagenEditable, Filtro


class EditorServicio:
    """Coordina las operaciones de edición sin acoplarse a la interfaz gráfica."""

    def __init__(self) -> None:
        self.__proyecto_actual: Optional[ImagenEditable] = None

    @property
    def hay_imagen_cargada(self) -> bool:
        return self.__proyecto_actual is not None

    @property
    def proyecto_actual(self) -> ImagenEditable:
        if self.__proyecto_actual is None:
            raise RuntimeError("No hay ninguna imagen cargada en el editor.")
        return self.__proyecto_actual

    def cargar_imagen(self, ruta_archivo: str) -> ImagenEditable:
        self.__proyecto_actual = ImagenEditable(ruta_archivo)
        return self.__proyecto_actual

    def aplicar_filtro(self, filtro: Filtro) -> Image.Image:
        proyecto = self.proyecto_actual
        if not isinstance(filtro, Filtro):
            raise TypeError("El parámetro debe ser una instancia de una subclase de Filtro.")

        imagen_procesada = filtro.aplicar(proyecto.imagen_actual)
        proyecto.actualizar_imagen(imagen_procesada)
        return proyecto.imagen_actual

    def deshacer_cambio(self) -> bool:
        return self.proyecto_actual.deshacer()

    def restaurar_original(self) -> Image.Image:
        proyecto = self.proyecto_actual
        proyecto.restaurar_original()
        return proyecto.imagen_actual

    def exportar_imagen(self, ruta_destino: str) -> None:
        self.proyecto_actual.guardar(ruta_destino)