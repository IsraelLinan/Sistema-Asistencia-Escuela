import tkinter as tk
from tkinter import ttk, messagebox
from colegio_lib import db_pool  # Importamos el pool de conexiones
from datetime import datetime
from PIL import Image, ImageTk  # Importar PIL para manejar la imagen

class StudentIngressModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Módulo Ingreso Estudiantes")
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

        # Etiqueta y campo de entrada para el código de barras
        self.barcode_label = ttk.Label(self, text="Código de Barras:")
        self.barcode_label.grid(row=1, column=0, sticky="W", pady=5)

        self.barcode_entry = ttk.Entry(self, width=30)
        self.barcode_entry.grid(row=1, column=1, pady=5)

        # Botón para registrar el ingreso
        self.register_btn = ttk.Button(self, text="Registrar Ingreso Estudiante", command=self.register_ingreso)
        self.register_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Etiqueta de estado
        self.status_label = ttk.Label(self, text="")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

    def register_ingreso(self):
        codigo = self.barcode_entry.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Ingrese un código de barras.")
            return

        try:
            # Obtener una conexión del pool
            conn = db_pool.get_conn()
            cur = conn.cursor()
            # Verificar si el estudiante existe
            cur.execute(
                "SELECT id, nombre FROM estudiantes WHERE codigo_barras = %s",
                (codigo,)
            )
            row = cur.fetchone()

            if row:
                estudiante_id, nombre = row
                # Registrar ingreso
                cur.execute(
                    "INSERT INTO ingresos_estudiantes (estudiante_id) VALUES (%s)",
                    (estudiante_id,)
                )
                conn.commit()
                hora = datetime.now().strftime('%H:%M:%S')
                self.status_label.config(
                    text=f"Ingreso registrado: {nombre} a las {hora}"
                )
            else:
                messagebox.showerror("Error", "Código no registrado.")

            cur.close()
            # Devolver la conexión al pool
            db_pool.put_conn(conn)

        except Exception as e:
            messagebox.showerror("Error BD", str(e))

        # Limpiar el campo
        self.barcode_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentIngressModule(root)
    app.pack(padx=10, pady=10)
    root.mainloop()



