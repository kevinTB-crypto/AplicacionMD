from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
import sqlite3

# ---------------- BASE DE DATOS ---------------- #


def crear_db():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad INTEGER,
        categoria TEXT
    )
    """)

    conexion.commit()
    conexion.close()


def guardar_datos(nombre, edad, categoria):
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO usuarios(nombre, edad, categoria) VALUES (?, ?, ?)",
        (nombre, edad, categoria),
    )

    conexion.commit()
    conexion.close()


# ---------------- FUNCIONES ---------------- #


def clasificar_edad(edad):
    if edad <= 12:
        return "Niño"
    elif edad <= 17:
        return "Adolescente"
    elif edad <= 59:
        return "Adulto"
    else:
        return "Adulto Mayor"


# ---------------- PANTALLA 1 ---------------- #


class Pantalla1(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)

        self.titulo = MDLabel(
            text="Registro de Usuario", halign="center", font_style="H4"
        )

        self.nombre = MDTextField(hint_text="Ingrese su nombre")

        self.edad = MDTextField(hint_text="Ingrese su edad")

        self.boton = MDRaisedButton(
            text="Validar y Continuar",
            pos_hint={"center_x": 0.5},
            on_release=self.validar,
        )

        layout.add_widget(self.titulo)
        layout.add_widget(self.nombre)
        layout.add_widget(self.edad)
        layout.add_widget(self.boton)

        self.add_widget(layout)

    def validar(self, obj):
        nombre = self.nombre.text.strip()
        edad = self.edad.text.strip()

        if nombre == "" or edad == "":
            Snackbar(text="Complete todos los campos").open()
            return

        if not edad.isdigit():
            Snackbar(text="La edad debe ser número").open()
            return

        edad = int(edad)

        categoria = clasificar_edad(edad)

        guardar_datos(nombre, edad, categoria)

        pantalla2 = self.manager.get_screen("pantalla2")

        pantalla2.ids_label.text = (
            f"Hola {nombre}\n" f"Tienes {edad} años\n" f"Categoría: {categoria}"
        )

        self.manager.current = "pantalla2"

        self.nombre.text = ""
        self.edad.text = ""


# ---------------- PANTALLA 2 ---------------- #


class Pantalla2(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=30)

        self.ids_label = MDLabel(text="", halign="center", font_style="H5")

        boton_regresar = MDRaisedButton(
            text="Regresar", pos_hint={"center_x": 0.5}, on_release=self.regresar
        )

        layout.add_widget(self.ids_label)
        layout.add_widget(boton_regresar)

        self.add_widget(layout)

    def regresar(self, obj):
        self.manager.current = "pantalla1"


# ---------------- APP ---------------- #


class MiApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"

        crear_db()

        sm = MDScreenManager()

        sm.add_widget(Pantalla1(name="pantalla1"))
        sm.add_widget(Pantalla2(name="pantalla2"))

        return sm


MiApp().run()
