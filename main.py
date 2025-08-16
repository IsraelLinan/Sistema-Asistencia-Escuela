import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk  # Importamos ThemedTk de ttkthemes
from datetime import datetime
from PIL import Image, ImageTk  # Importar PIL para manejar la imagen
from student_ingress_module import StudentIngressModule
from teacher_ingress_module import TeacherIngressModule
from weekly_reports_module import WeeklyReportsModule
from generador_codigo import GeneradorCodigo  

class MainApplication(ThemedTk):  # Usamos ThemedTk para aplicar el tema
    def __init__(self):
        super().__init__()
        # Establece el tamaño de la ventana
        width = 350
        height = 450

        # Centra la ventana en la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Fija el tamaño para que no se pueda redimensionar
        self.resizable(False, False)
        self.title("Sistema de Gestión Escolar")
        self.set_theme('plastik')  # Usamos el tema 'plastik'
        self.create_widgets()

    def create_widgets(self):
        # Cargar y mostrar la imagen del logo
        logo_path = "logo_colegio.png"  # Ruta de la imagen
        logo = Image.open(logo_path)  # Abrir la imagen
        logo = logo.resize((100, 100), Image.Resampling.LANCZOS)  # Usamos la nueva constante LANCZOS
        logo_image = ImageTk.PhotoImage(logo)  # Convertir la imagen a un formato que Tkinter pueda usar

        logo_label = ttk.Label(self, image=logo_image)
        logo_label.image = logo_image  # Guardar una referencia a la imagen
        logo_label.pack(pady=(20, 10))  # Mayor espacio arriba y menos abajo

        # Titulo y fecha/hora
        title_label = ttk.Label(self, text="Sistema de Asistencia Escolar", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(10, 5))  # Más espacio arriba, menos abajo

        now = datetime.now()
        date_label = ttk.Label(self, text=now.strftime("%d, %B %Y, %H:%M:%S"), font=('Arial', 12))
        date_label.pack(pady=(0, 20))  # Espacio solo abajo para separar de los botones

        # Botones con tamaño más compacto y espaciado ajustado
        self.student_button = ttk.Button(self, text="Ingreso de Estudiante", command=self.open_student_module, width=20)
        self.student_button.pack(pady=10)

        self.teacher_button = ttk.Button(self, text="Ingreso del Docente", command=self.open_teacher_module, width=20)
        self.teacher_button.pack(pady=10)

        self.report_button = ttk.Button(self, text="Reporte de Asistencia", command=self.open_report_module, width=20)
        self.report_button.pack(pady=10)

        # Botón para abrir el generador de código de barra
        self.barcode_button = ttk.Button(self, text="Generar Código Barra", command=self.open_barcode_module, width=20)
        self.barcode_button.pack(pady=10)

    def open_student_module(self):
        student_window = tk.Toplevel(self)
        student_window.title("Ingreso de Estudiantes")
        app = StudentIngressModule(student_window)
        app.pack(fill='both', expand=True, padx=10, pady=10)

    def open_teacher_module(self):
        teacher_window = tk.Toplevel(self)
        teacher_window.title("Ingreso de Docentes")
        app = TeacherIngressModule(teacher_window)
        app.pack(fill='both', expand=True, padx=10, pady=10)

    def open_report_module(self):
        report_window = tk.Toplevel(self)
        report_window.title("Reporte de Asistencias")
        app = WeeklyReportsModule(report_window)
        app.pack(fill='both', expand=True, padx=10, pady=10)

    def open_barcode_module(self):
        barcode_window = tk.Toplevel(self)
        barcode_window.title("Generador Código de Barra")
        app = GeneradorCodigo(barcode_window)  # Abre el módulo de generador de código de barra
        app.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()











