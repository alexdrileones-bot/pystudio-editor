from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

from servicios import EditorServicio
from modelos import (
    Filtro,
    FiltroEscalaGrises,
    FiltroDesenfoque,
    FiltroContraste,
    FiltroRotacion,
)


class VentanaPrincipal(ctk.CTk):
    """Interfaz gráfica principal de PyStudio construida con CustomTkinter."""

    ANCHO_MAX_PREVIEW = 680
    ALTO_MAX_PREVIEW = 520

    def __init__(self, servicio: EditorServicio) -> None:
        super().__init__()

        self.__servicio: EditorServicio = servicio
        self.__ctk_imagen_actual: ctk.CTkImage | None = None

        self.__configurar_ventana()
        self.__construir_interfaz()
        self.__actualizar_estado_controles()

    def __configurar_ventana(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("PyStudio — Editor de Imágenes POO")
        self.geometry("1040x680")
        self.minsize(900, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def __construir_interfaz(self) -> None:
        panel_lateral = ctk.CTkFrame(self, width=280, corner_radius=0)
        panel_lateral.grid(row=0, column=0, rowspan=2, sticky="nsew")
        panel_lateral.grid_propagate(False)

        titulo = ctk.CTkLabel(
            panel_lateral,
            text="PyStudio",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        titulo.pack(pady=(20, 4))

        subtitulo = ctk.CTkLabel(
            panel_lateral,
            text="Editor Orientado a Objetos",
            font=ctk.CTkFont(size=12),
            text_color="gray70",
        )
        subtitulo.pack(pady=(0, 18))

        self.__btn_abrir = ctk.CTkButton(
            panel_lateral, text="📂 Abrir Imagen", command=self.__evento_abrir_imagen
        )
        self.__btn_abrir.pack(padx=20, pady=6, fill="x")

        self.__btn_guardar = ctk.CTkButton(
            panel_lateral,
            text="💾 Exportar Imagen",
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self.__evento_guardar_imagen,
        )
        self.__btn_guardar.pack(padx=20, pady=6, fill="x")

        frame_historial = ctk.CTkFrame(panel_lateral, fg_color="transparent")
        frame_historial.pack(padx=20, pady=(10, 15), fill="x")
        frame_historial.grid_columnconfigure((0, 1), weight=1)

        self.__btn_deshacer = ctk.CTkButton(
            frame_historial,
            text="↩ Deshacer",
            fg_color="gray30",
            hover_color="gray20",
            command=self.__evento_deshacer,
        )
        self.__btn_deshacer.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        self.__btn_restaurar = ctk.CTkButton(
            frame_historial,
            text="⟲ Original",
            fg_color="gray30",
            hover_color="gray20",
            command=self.__evento_restaurar,
        )
        self.__btn_restaurar.grid(row=0, column=1, padx=(4, 0), sticky="ew")

        ctk.CTkLabel(
            panel_lateral,
            text="FILTROS DISPONIBLES",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray75",
        ).pack(pady=(10, 8))

        self.__btn_grises = ctk.CTkButton(
            panel_lateral,
            text="Escala de Grises",
            command=lambda: self.__ejecutar_filtro(FiltroEscalaGrises()),
        )
        self.__btn_grises.pack(padx=20, pady=6, fill="x")

        self.__btn_rotar = ctk.CTkButton(
            panel_lateral,
            text="Rotar 90° Horario",
            command=lambda: self.__ejecutar_filtro(FiltroRotacion(90)),
        )
        self.__btn_rotar.pack(padx=20, pady=6, fill="x")

        self.__lbl_desenfoque = ctk.CTkLabel(panel_lateral, text="Desenfoque (Radio: 2.5)")
        self.__lbl_desenfoque.pack(padx=20, pady=(14, 0), anchor="w")

        self.__slider_desenfoque = ctk.CTkSlider(
            panel_lateral,
            from_=0.5,
            to=15.0,
            number_of_steps=29,
            command=self.__actualizar_etiqueta_desenfoque,
        )
        self.__slider_desenfoque.set(2.5)
        self.__slider_desenfoque.pack(padx=20, pady=4, fill="x")

        self.__btn_desenfoque = ctk.CTkButton(
            panel_lateral,
            text="Aplicar Desenfoque",
            command=self.__evento_aplicar_desenfoque,
        )
        self.__btn_desenfoque.pack(padx=20, pady=(2, 10), fill="x")

        self.__lbl_contraste = ctk.CTkLabel(panel_lateral, text="Contraste (Factor: 1.4)")
        self.__lbl_contraste.pack(padx=20, pady=(8, 0), anchor="w")

        self.__slider_contraste = ctk.CTkSlider(
            panel_lateral,
            from_=0.2,
            to=3.0,
            number_of_steps=28,
            command=self.__actualizar_etiqueta_contraste,
        )
        self.__slider_contraste.set(1.4)
        self.__slider_contraste.pack(padx=20, pady=4, fill="x")

        self.__btn_contraste = ctk.CTkButton(
            panel_lateral,
            text="Aplicar Contraste",
            command=self.__evento_aplicar_contraste,
        )
        self.__btn_contraste.pack(padx=20, pady=(2, 10), fill="x")

        marco_visor = ctk.CTkFrame(self, fg_color="#181818", corner_radius=12)
        marco_visor.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")
        marco_visor.grid_rowconfigure(0, weight=1)
        marco_visor.grid_columnconfigure(0, weight=1)

        self.__lbl_visor = ctk.CTkLabel(
            marco_visor,
            text="Haz clic en 'Abrir Imagen' para comenzar a editar",
            font=ctk.CTkFont(size=15),
            text_color="gray60",
        )
        self.__lbl_visor.grid(row=0, column=0, padx=15, pady=15)

        self.__lbl_estado = ctk.CTkLabel(
            self,
            text="Sin imagen cargada",
            font=ctk.CTkFont(size=12),
            text_color="gray75",
            anchor="w",
        )
        self.__lbl_estado.grid(row=1, column=1, padx=22, pady=(0, 12), sticky="ew")

    def __actualizar_etiqueta_desenfoque(self, valor: float) -> None:
        self.__lbl_desenfoque.configure(text=f"Desenfoque (Radio: {valor:.1f})")

    def __actualizar_etiqueta_contraste(self, valor: float) -> None:
        self.__lbl_contraste.configure(text=f"Contraste (Factor: {valor:.1f})")

    def __evento_abrir_imagen(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes soportadas", "*.png *.jpg *.jpeg *.bmp *.webp"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if not ruta:
            return

        try:
            proyecto = self.__servicio.cargar_imagen(ruta)
            self.__renderizar_imagen(proyecto.imagen_actual)
            self.__actualizar_estado_controles()
        except (FileNotFoundError, ValueError, Exception) as error:
            messagebox.showerror("Error al abrir imagen", str(error))

    def __ejecutar_filtro(self, filtro: Filtro) -> None:
        try:
            imagen_resultante = self.__servicio.aplicar_filtro(filtro)
            self.__renderizar_imagen(imagen_resultante)
            self.__actualizar_estado_controles(f"Filtro aplicado: {filtro.nombre}")
        except (RuntimeError, ValueError, TypeError) as error:
            messagebox.showerror("Error al aplicar filtro", str(error))

    def __evento_aplicar_desenfoque(self) -> None:
        radio = round(self.__slider_desenfoque.get(), 1)
        self.__ejecutar_filtro(FiltroDesenfoque(radio=radio))

    def __evento_aplicar_contraste(self) -> None:
        factor = round(self.__slider_contraste.get(), 1)
        self.__ejecutar_filtro(FiltroContraste(factor=factor))

    def __evento_deshacer(self) -> None:
        try:
            if self.__servicio.deshacer_cambio():
                self.__renderizar_imagen(self.__servicio.proyecto_actual.imagen_actual)
                self.__actualizar_estado_controles("Último cambio deshecho")
        except RuntimeError as error:
            messagebox.showwarning("Aviso", str(error))

    def __evento_restaurar(self) -> None:
        try:
            imagen_original = self.__servicio.restaurar_original()
            self.__renderizar_imagen(imagen_original)
            self.__actualizar_estado_controles("Imagen restaurada al estado original")
        except RuntimeError as error:
            messagebox.showwarning("Aviso", str(error))

    def __evento_guardar_imagen(self) -> None:
        ruta_destino = filedialog.asksaveasfilename(
            title="Exportar imagen editada",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("WEBP", "*.webp"),
            ],
        )
        if not ruta_destino:
            return

        try:
            self.__servicio.exportar_imagen(ruta_destino)
            messagebox.showinfo("Exportación exitosa", "La imagen se guardó correctamente.")
        except (RuntimeError, ValueError, Exception) as error:
            messagebox.showerror("Error al exportar", str(error))

    def __renderizar_imagen(self, imagen_pil: Image.Image) -> None:
        ancho, alto = imagen_pil.size
        escala = min(
            self.ANCHO_MAX_PREVIEW / ancho,
            self.ALTO_MAX_PREVIEW / alto,
            1.0,
        )
        nuevo_tamano = (int(ancho * escala), int(alto * escala))

        self.__ctk_imagen_actual = ctk.CTkImage(
            light_image=imagen_pil,
            dark_image=imagen_pil,
            size=nuevo_tamano,
        )
        self.__lbl_visor.configure(image=self.__ctk_imagen_actual, text="")

    def __actualizar_estado_controles(self, mensaje_extra: str = "") -> None:
        hay_imagen = self.__servicio.hay_imagen_cargada
        estado_botones = "normal" if hay_imagen else "disabled"

        for boton in (
            self.__btn_guardar,
            self.__btn_restaurar,
            self.__btn_grises,
            self.__btn_rotar,
            self.__btn_desenfoque,
            self.__btn_contraste,
        ):
            boton.configure(state=estado_botones)

        if hay_imagen:
            proyecto = self.__servicio.proyecto_actual
            estado_deshacer = "normal" if proyecto.puede_deshacer else "disabled"
            self.__btn_deshacer.configure(state=estado_deshacer)

            ancho, alto = proyecto.dimensiones
            info = f"Archivo: {proyecto.nombre_archivo}  |  Resolución: {ancho}x{alto} px"
            if mensaje_extra:
                info += f"  |  {mensaje_extra}"
            self.__lbl_estado.configure(text=info)
        else:
            self.__btn_deshacer.configure(state="disabled")
            self.__lbl_estado.configure(text="Sin imagen cargada")