import tkinter as tk
from tkinter import ttk, messagebox
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import hashlib
from colegio_lib import db_pool  # Importamos la conexión a la base de datos

class GeneradorCodigo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Generador de Códigos de Barra")
        self.style = ttk.Style()
        self.style.theme_use('plastik')  # Aplicamos el tema 'plastik'
        self.create_widgets()

    def create_widgets(self):
        # Cargar y mostrar la imagen del logo
        logo_path = "logo_colegio.png"  # Ruta de la imagen
        logo = Image.open(logo_path)  # Abrir la imagen
        logo = logo.resize((100, 100), Image.Resampling.LANCZOS)  # Ajustar el tamaño de la imagen
        logo_image = ImageTk.PhotoImage(logo)  # Convertir la imagen a un formato que Tkinter pueda usar

        logo_label = ttk.Label(self, image=logo_image)
        logo_label.image = logo_image  # Guardar una referencia a la imagen
        logo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiqueta y campo de entrada para el nombre
        self.name_label = ttk.Label(self, text="Nombre Completo:")
        self.name_label.grid(row=1, column=0, sticky="W", pady=5)

        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.grid(row=1, column=1, pady=5)

        # ComboBox para seleccionar tipo de persona (Estudiante o Docente)
        self.type_label = ttk.Label(self, text="Seleccione:")
        self.type_label.grid(row=2, column=0, sticky="W", pady=5)

        self.type_combobox = ttk.Combobox(self, values=["Estudiante", "Docente"], state="readonly", width=28)
        self.type_combobox.grid(row=2, column=1, pady=5)
        self.type_combobox.set("Estudiante")  # Valor predeterminado

        # Botón para generar el código de barra
        self.generate_btn = ttk.Button(self, text="Generar Código de Barra", command=self.generate_barcode)
        self.generate_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Imagen del código de barra
        self.barcode_image_label = ttk.Label(self, text="Código de Barra generado aparecerá aquí.")
        self.barcode_image_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Botón para imprimir el código de barra
        self.print_btn = ttk.Button(self, text="Imprimir Código de Barra", command=self.print_barcode)
        self.print_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.barcode_image = None  # Variable para almacenar la imagen del código de barra

    def generate_barcode(self):
        # Obtener el nombre completo del estudiante o docente
        name = self.name_entry.get().strip()
        person_type = self.type_combobox.get()

        if not name:
            messagebox.showwarning("Atención", "Ingrese un nombre completo.")
            return

        # Generar un código de barras único basado en el nombre
        unique_id = hashlib.md5(name.encode()).hexdigest()

        try:
            # Conectar a la base de datos
            conn = db_pool.get_conn()
            cur = conn.cursor()

            # Insertar la persona en la tabla 'personas' (tabla general)
            cur.execute(
                "INSERT INTO personas (nombre_completo, codigo_barras, tipo_persona) VALUES (%s, %s, %s)",
                (name, unique_id, person_type)
            )
            conn.commit()

            # Dependiendo del tipo, insertar en la tabla específica (estudiantes o docentes)
            if person_type == "Estudiante":
                cur.execute(
                    "INSERT INTO estudiantes (nombre, codigo_barras) VALUES (%s, %s)",
                    (name, unique_id)
                )
            elif person_type == "Docente":
                cur.execute(
                    "INSERT INTO docentes (nombre, codigo_barras) VALUES (%s, %s)",
                    (name, unique_id)
                )

            # Confirmar la inserción
            conn.commit()

            # Cerrar la conexión
            cur.close()
            # Devolver la conexión al pool
            db_pool.put_conn(conn)

            # Generar el código de barras
            barcode_object = barcode.get_barcode_class('code128')(unique_id, writer=ImageWriter())
            barcode_image = barcode_object.render()

            # Mostrar la imagen del código de barra
            self.barcode_image = barcode_image
            self.barcode_image_label.config(text="Código de Barra generado.")
            self.barcode_image.show()

        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    def print_barcode(self):
        if self.barcode_image:
            # Imprimir la imagen del código de barra
            self.barcode_image.show()  # Esto abrirá la imagen para su impresión por el visor predeterminado del sistema
        else:
            messagebox.showwarning("Atención", "Primero genere un código de barra.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorCodigo(root)
    app.pack(padx=10, pady=10)
    root.mainloop()





