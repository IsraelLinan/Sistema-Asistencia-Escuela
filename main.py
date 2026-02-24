import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
from student_ingress_module import StudentIngressModule
from teacher_ingress_module import TeacherIngressModule
from weekly_reports_module import WeeklyReportsModule
from generador_codigo import GeneradorCodigo
from colegio_lib import COLORS
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Escolar")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(True, True)

        # Tamaño y centrado
        width, height = 420, 660
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

        self._build_ui()
        self._update_clock()

    def _build_ui(self):
        # ── Logo y marca ─────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=0)
        header.pack(fill="x")

        inner = ctk.CTkFrame(header, fg_color="transparent")
        inner.pack(pady=28)

        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("logo_colegio.png"),
                dark_image=Image.open("logo_colegio.png"),
                size=(90, 90)
            )
            ctk.CTkLabel(inner, image=logo_img, text="").pack()
        except Exception:
            ctk.CTkLabel(inner, text="🏫", font=("Segoe UI", 52)).pack()

        ctk.CTkLabel(inner, text="Sistema de Gestión Escolar",
                     font=ctk.CTkFont("Segoe UI", 16, "bold"),
                     text_color=COLORS["text"]).pack(pady=(10, 2))

        self.clock_label = ctk.CTkLabel(inner, text="",
                                         font=ctk.CTkFont("Segoe UI", 11),
                                         text_color=COLORS["text_muted"])
        self.clock_label.pack()

        # ── Divisor ───────────────────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, fg_color=COLORS["border"]).pack(fill="x")

        # ── Menú de navegación ────────────────────────────────────────────────
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="both", expand=True, padx=28, pady=24)

        ctk.CTkLabel(nav, text="MÓDULOS",
                     font=ctk.CTkFont("Segoe UI", 9, "bold"),
                     text_color=COLORS["text_muted"]).pack(anchor="w", pady=(0, 10))

        # Definición de botones: (icono, texto, comando, color_acento)
        buttons = [
            ("🎓", "Registro de Estudiantes",  self.open_student_module,   COLORS["accent"]),
            ("👨‍🏫", "Registro de Docentes",     self.open_teacher_module,   "#22c55e"),
            ("📋", "Reporte de Asistencia",    self.open_report_module,    "#f59e0b"),
            ("🏷️", "Generar Código de Barra",  self.open_barcode_module,   "#a855f7"),
        ]

        for icon, label, cmd, color in buttons:
            self._nav_button(nav, icon, label, cmd, color)

        # Separador antes del dashboard
        ctk.CTkFrame(nav, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=(14, 14))

        ctk.CTkLabel(nav, text="HERRAMIENTAS",
                     font=ctk.CTkFont("Segoe UI", 9, "bold"),
                     text_color=COLORS["text_muted"]).pack(anchor="w", pady=(0, 10))

        self._nav_button(nav, "📊", "Abrir Dashboard Web", self.open_dashboard, "#ef4444")

        # ── Pie ───────────────────────────────────────────────────────────────
        ctk.CTkLabel(self, text="v2.0  •  Sistema Escolar",
                     font=ctk.CTkFont("Segoe UI", 9),
                     text_color=COLORS["border"]).pack(pady=(0, 14))

    def _nav_button(self, parent, icon, label, command, accent_color):
        """Crea un botón de navegación con estilo de fila."""
        # Contenedor externo para la barra de color + botón
        row = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        row.pack(fill="x", pady=4)
        row.pack_propagate(False)

        # Barra de color lateral
        indicator = ctk.CTkFrame(row, width=5, corner_radius=3, fg_color=accent_color)
        indicator.pack(side="left", fill="y", padx=(0, 0))

        # Botón principal
        btn = ctk.CTkButton(
            row,
            text=f"  {icon}   {label}",
            anchor="w",
            height=46,
            corner_radius=10,
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            fg_color=COLORS["bg2"],
            hover_color=COLORS["bg3"],
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            command=command
        )
        btn.pack(side="left", fill="both", expand=True)

    def _update_clock(self):
        now = datetime.now().strftime("%A %d de %B, %Y   %H:%M:%S")
        self.clock_label.configure(text=now)
        self.after(1000, self._update_clock)

    # ── Abrir módulos en ventanas secundarias ─────────────────────────────────

    def _open_module(self, title, ModuleClass, size="700x560"):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.configure(fg_color=COLORS["bg"])
        win.geometry(size)
        win.resizable(True, True)
        # Centrar la ventana secundaria
        win.update_idletasks()
        w, h = map(int, size.split("x"))
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        win.lift()
        win.focus_force()
        module = ModuleClass(win)
        module.pack(fill="both", expand=True)
        return win

    def open_student_module(self):
        self._open_module("Asistencia de Estudiantes", StudentIngressModule, "680x580")

    def open_teacher_module(self):
        self._open_module("Asistencia de Docentes", TeacherIngressModule, "680x580")

    def open_report_module(self):
        self._open_module("Reporte de Asistencias", WeeklyReportsModule, "920x660")

    def open_barcode_module(self):
        self._open_module("Generador de Código de Barra", GeneradorCodigo, "580x640")

    def open_dashboard(self):
        try:
            subprocess.Popen(["streamlit", "run", "dashboard.py"])
            # Feedback visual al usuario
            btn_feedback = ctk.CTkToplevel(self)
            btn_feedback.title("")
            btn_feedback.configure(fg_color=COLORS["bg2"])
            btn_feedback.geometry("320x120")
            btn_feedback.resizable(False, False)
            sw, sh = btn_feedback.winfo_screenwidth(), btn_feedback.winfo_screenheight()
            btn_feedback.geometry(f"320x120+{(sw-320)//2}+{(sh-120)//2}")
            ctk.CTkLabel(btn_feedback, text="✔  Dashboard iniciándose...",
                         font=ctk.CTkFont("Segoe UI", 13, "bold"),
                         text_color=COLORS["success"]).pack(pady=(28, 4))
            ctk.CTkLabel(btn_feedback, text="Se abrirá en tu navegador en unos segundos.",
                         font=ctk.CTkFont("Segoe UI", 10),
                         text_color=COLORS["text_muted"]).pack()
            btn_feedback.after(3000, btn_feedback.destroy)
        except FileNotFoundError:
            messagebox.showerror("Error", "Streamlit no está instalado o no está en el PATH.\n"
                                          "Instálalo con: pip install streamlit")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el dashboard:\n{e}")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()










