import os
from abc import ABC, abstractmethod
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


class ImagenEditable:
    """Representa una imagen cargada en el editor y protege su estado interno."""

    FORMATOS_SOPORTADOS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
    MAX_HISTORIAL = 10

    def __init__(self, ruta_archivo: str) -> None:
        self.__validar_ruta(ruta_archivo)
        self.__ruta_archivo: str = ruta_archivo

        imagen_base = Image.open(ruta_archivo).convert("RGB")
        self.__imagen_original: Image.Image = imagen_base.copy()
        self.__imagen_actual: Image.Image = imagen_base.copy()
        self.__historial: list[Image.Image] = []

    @staticmethod
    def __validar_ruta(ruta: str) -> None:
        if not ruta or not os.path.isfile(ruta):
            raise FileNotFoundError(f"No se encontró el archivo en la ruta: {ruta}")

        extension = os.path.splitext(ruta)[1].lower()
        if extension not in ImagenEditable.FORMATOS_SOPORTADOS:
            raise ValueError(
                f"Formato '{extension}' no soportado. Use: {', '.join(ImagenEditable.FORMATOS_SOPORTADOS)}"
            )

    @property
    def ruta_archivo(self) -> str:
        return self.__ruta_archivo

    @property
    def nombre_archivo(self) -> str:
        return os.path.basename(self.__ruta_archivo)

    @property
    def imagen_actual(self) -> Image.Image:
        return self.__imagen_actual.copy()

    @property
    def dimensiones(self) -> tuple[int, int]:
        return self.__imagen_actual.size

    @property
    def puede_deshacer(self) -> bool:
        return len(self.__historial) > 0

    def actualizar_imagen(self, nueva_imagen: Image.Image) -> None:
        if not isinstance(nueva_imagen, Image.Image):
            raise TypeError("El objeto proporcionado no es una imagen válida de Pillow.")

        if len(self.__historial) >= self.MAX_HISTORIAL:
            self.__historial.pop(0)

        self.__historial.append(self.__imagen_actual.copy())
        self.__imagen_actual = nueva_imagen.copy()

    def deshacer(self) -> bool:
        if not self.puede_deshacer:
            return False
        self.__imagen_actual = self.__historial.pop()
        return True

    def restaurar_original(self) -> None:
        self.__historial.clear()
        self.__imagen_actual = self.__imagen_original.copy()

    def guardar(self, ruta_destino: str) -> None:
        if not ruta_destino:
            raise ValueError("La ruta de destino no puede estar vacía.")

        extension = os.path.splitext(ruta_destino)[1].lower()
        if extension not in self.FORMATOS_SOPORTADOS:
            raise ValueError(
                f"Extensión de salida '{extension}' inválida. Use: {', '.join(self.FORMATOS_SOPORTADOS)}"
            )

        self.__imagen_actual.save(ruta_destino)


class Filtro(ABC):
    """Clase abstracta base que define el contrato para cualquier filtro de imagen."""

    def __init__(self, nombre: str) -> None:
        self._nombre: str = nombre

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def aplicar(self, imagen: Image.Image) -> Image.Image:
        """Aplica una transformación sobre la imagen y retorna el resultado."""
        pass


class FiltroEscalaGrises(Filtro):
    """Convierte la imagen a escala de grises manteniendo 3 canales RGB."""

    def __init__(self) -> None:
        super().__init__("Escala de Grises")

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        return ImageOps.grayscale(imagen).convert("RGB")


class FiltroDesenfoque(Filtro):
    """Aplica un desenfoque gaussiano configurable mediante radio."""

    def __init__(self, radio: float = 2.5) -> None:
        super().__init__("Desenfoque Gaussiano")
        self.radio = radio

    @property
    def radio(self) -> float:
        return self.__radio

    @radio.setter
    def radio(self, valor: float) -> None:
        if not (0.1 <= valor <= 20.0):
            raise ValueError("El radio de desenfoque debe estar entre 0.1 y 20.0.")
        self.__radio = float(valor)

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        return imagen.filter(ImageFilter.GaussianBlur(radius=self.__radio))


class FiltroContraste(Filtro):
    """Ajusta el nivel de contraste de la imagen según un factor."""

    def __init__(self, factor: float = 1.4) -> None:
        super().__init__("Ajuste de Contraste")
        self.factor = factor

    @property
    def factor(self) -> float:
        return self.__factor

    @factor.setter
    def factor(self, valor: float) -> None:
        if not (0.1 <= valor <= 5.0):
            raise ValueError("El factor de contraste debe estar entre 0.1 y 5.0.")
        self.__factor = float(valor)

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        realzador = ImageEnhance.Contrast(imagen)
        return realzador.enhance(self.__factor)


class FiltroRotacion(Filtro):
    """Rota la imagen en sentido horario según los grados indicados."""

    def __init__(self, grados: int = 90) -> None:
        super().__init__("Rotación")
        self.grados = grados

    @property
    def grados(self) -> int:
        return self.__grados

    @grados.setter
    def grados(self, valor: int) -> None:
        if valor == 0 or not (-360 <= valor <= 360):
            raise ValueError("Los grados de rotación deben estar entre -360 y 360 (distinto de 0).")
        self.__grados = int(valor)

    def aplicar(self, imagen: Image.Image) -> Image.Image:
        return imagen.rotate(-self.__grados, expand=True)