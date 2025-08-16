import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from colegio_lib import db_pool
from main import MainApplication

class LoginScreen(ThemedTk):
    def __init__(self):
        super().__init__(theme="plastik")
        self.title("Login - Sistema de Gestión Escolar")

        # Tamaño fijo y centrado
        width = 400   #ancho
        height = 450  #alto
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=20)

        # Logo
        try:
            logo = Image.open("logo_colegio.png")
            logo = logo.resize((220, 220), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(logo)
            logo_label = ttk.Label(frame, image=logo_img)
            logo_label.image = logo_img
            logo_label.pack()
        except Exception as e:
            print("No se pudo cargar el logo:", e)

        ttk.Label(frame, text="Usuario:").pack(pady=(20, 5))
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack()

        ttk.Label(frame, text="Contraseña:").pack(pady=(10, 5))
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack()

        ttk.Button(frame, text="Iniciar Sesión", command=self.verify_login).pack(pady=15)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            conn = db_pool.get_conn()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password))
            result = cur.fetchone()
            cur.close()
            db_pool.put_conn(conn)

            if result:
                self.destroy()
                app = MainApplication()
                app.mainloop()
            else:
                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar usuario: {e}")

if __name__ == "__main__":
    login = LoginScreen()
    login.mainloop()

