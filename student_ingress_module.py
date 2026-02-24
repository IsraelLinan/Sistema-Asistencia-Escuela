import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from colegio_lib import db_pool, COLORS
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class StudentIngressModule(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.parent = parent
        if isinstance(parent, ctk.CTk) or isinstance(parent, ctk.CTkToplevel):
            self.parent.title("Módulo Registro Estudiantes")
        self._build_ui()

    def _build_ui(self):
        # ── Encabezado ──────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=14,
                              border_width=1, border_color=COLORS["border"])
        header.pack(fill="x", padx=20, pady=(20, 10))

        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("logo_colegio.png"),
                dark_image=Image.open("logo_colegio.png"),
                size=(70, 70)
            )
            ctk.CTkLabel(header, image=logo_img, text="").pack(side="left", padx=18, pady=12)
        except Exception:
            ctk.CTkLabel(header, text="🎓", font=("Segoe UI", 36)).pack(side="left", padx=18, pady=12)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left", pady=12)
        ctk.CTkLabel(title_box, text="Registro de Estudiantes",
                     font=ctk.CTkFont("Segoe UI", 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Ingreso y salida mediante código de barras",
                     font=ctk.CTkFont("Segoe UI", 11),
                     text_color=COLORS["text_muted"]).pack(anchor="w")

        # ── Panel principal ──────────────────────────────────────────────────
        main = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=14,
                            border_width=1, border_color=COLORS["border"])
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Fecha y hora en tiempo real
        self.datetime_label = ctk.CTkLabel(main, text="",
                                           font=ctk.CTkFont("Segoe UI", 11),
                                           text_color=COLORS["text_muted"])
        self.datetime_label.pack(pady=(18, 4))
        self._update_clock()

        # Separador visual
        sep = ctk.CTkFrame(main, height=1, fg_color=COLORS["border"])
        sep.pack(fill="x", padx=30, pady=(4, 20))

        # Ícono escáner
        ctk.CTkLabel(main, text="▤", font=("Segoe UI", 42),
                     text_color=COLORS["accent"]).pack()
        ctk.CTkLabel(main, text="Escanee o ingrese el código de barras",
                     font=ctk.CTkFont("Segoe UI", 12),
                     text_color=COLORS["text_muted"]).pack(pady=(4, 16))

        # Entry código
        self.barcode_entry = ctk.CTkEntry(
            main, placeholder_text="Código de barras...",
            height=46, corner_radius=10, width=320,
            font=ctk.CTkFont("Consolas", 13),
            fg_color=COLORS["bg3"], border_color=COLORS["accent"],
            text_color=COLORS["text"]
        )
        self.barcode_entry.pack(pady=(0, 22))
        self.barcode_entry.focus()
        self.barcode_entry.bind("<Return>", lambda e: self.register_ingreso())

        # Botones
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        ctk.CTkButton(
            btn_frame, text="▶  Registrar Ingreso", width=200, height=44,
            corner_radius=10, font=ctk.CTkFont("Segoe UI", 12, "bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self.register_ingreso
        ).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            btn_frame, text="◀  Registrar Salida", width=200, height=44,
            corner_radius=10, font=ctk.CTkFont("Segoe UI", 12, "bold"),
            fg_color=COLORS["bg3"], hover_color=COLORS["border"],
            border_width=1, border_color=COLORS["border"],
            command=self.register_salida
        ).grid(row=0, column=1, padx=8)

        # Panel de estado / historial
        sep2 = ctk.CTkFrame(main, height=1, fg_color=COLORS["border"])
        sep2.pack(fill="x", padx=30, pady=(8, 14))

        ctk.CTkLabel(main, text="Último registro",
                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     text_color=COLORS["text_muted"]).pack()

        self.status_card = ctk.CTkFrame(main, fg_color=COLORS["bg3"],
                                        corner_radius=10, height=60)
        self.status_card.pack(fill="x", padx=30, pady=(6, 20))
        self.status_card.pack_propagate(False)

        self.status_label = ctk.CTkLabel(self.status_card, text="Sin registros aún",
                                          font=ctk.CTkFont("Segoe UI", 12),
                                          text_color=COLORS["text_muted"])
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

    def _update_clock(self):
        now = datetime.now().strftime("%A, %d de %B de %Y  —  %H:%M:%S")
        self.datetime_label.configure(text=now)
        self.after(1000, self._update_clock)

    def _set_status(self, msg, color):
        self.status_label.configure(text=msg, text_color=color)
        self.status_card.configure(fg_color=COLORS["bg3"])

    def register_ingreso(self):
        codigo = self.barcode_entry.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Ingrese un código de barras.")
            return
        try:
            conn = db_pool.get_conn()
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM estudiantes WHERE codigo_barras = %s", (codigo,))
            row = cur.fetchone()
            if row:
                estudiante_id, nombre = row
                cur.execute("INSERT INTO ingresos_estudiantes (estudiante_id) VALUES (%s)", (estudiante_id,))
                conn.commit()
                hora = datetime.now().strftime('%H:%M:%S')
                self._set_status(f"✔  Ingreso: {nombre}  —  {hora}", COLORS["success"])
            else:
                self._set_status("✗  Código no registrado en el sistema.", COLORS["danger"])
            cur.close()
            db_pool.put_conn(conn)
        except Exception as e:
            messagebox.showerror("Error BD", str(e))
        self.barcode_entry.delete(0, "end")

    def register_salida(self):
        codigo = self.barcode_entry.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Ingrese un código de barras.")
            return
        try:
            conn = db_pool.get_conn()
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM estudiantes WHERE codigo_barras = %s", (codigo,))
            row = cur.fetchone()
            if not row:
                self._set_status("✗  Código no registrado en el sistema.", COLORS["danger"])
                cur.close()
                db_pool.put_conn(conn)
                self.barcode_entry.delete(0, "end")
                return
            estudiante_id, nombre = row
            cur.execute(
                "SELECT id FROM ingresos_estudiantes WHERE estudiante_id = %s AND hora_salida IS NULL ORDER BY hora_ingreso DESC LIMIT 1",
                (estudiante_id,)
            )
            ingreso_row = cur.fetchone()
            if ingreso_row:
                cur.execute("UPDATE ingresos_estudiantes SET hora_salida = %s WHERE id = %s",
                            (datetime.now(), ingreso_row[0]))
                conn.commit()
                hora = datetime.now().strftime('%H:%M:%S')
                self._set_status(f"◀  Salida: {nombre}  —  {hora}", COLORS["warning"])
            else:
                self._set_status("⚠  No hay ingreso pendiente para este estudiante.", COLORS["warning"])
            cur.close()
            db_pool.put_conn(conn)
        except Exception as e:
            messagebox.showerror("Error BD", str(e))
        self.barcode_entry.delete(0, "end")


if __name__ == "__main__":
    root = ctk.CTk()
    root.configure(fg_color=COLORS["bg"])
    root.geometry("640x520")
    app = StudentIngressModule(root)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()



