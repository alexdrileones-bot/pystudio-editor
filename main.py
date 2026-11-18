from servicios import EditorServicio
from interfaz import VentanaPrincipal


def main() -> None:
    servicio = EditorServicio()
    app = VentanaPrincipal(servicio)
    app.mainloop()


if __name__ == "__main__":
    main()