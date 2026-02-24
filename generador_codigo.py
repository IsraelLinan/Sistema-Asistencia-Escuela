import customtkinter as ctk
from tkinter import messagebox
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import hashlib
from colegio_lib import db_pool, COLORS

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GeneradorCodigo(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.parent = parent
        if isinstance(parent, ctk.CTk) or isinstance(parent, ctk.CTkToplevel):
            self.parent.title("Generador de Códigos de Barra")
        self.barcode_image = None
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
            ctk.CTkLabel(header, text="🏷️", font=("Segoe UI", 36)).pack(side="left", padx=18, pady=12)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left", pady=12)
        ctk.CTkLabel(title_box, text="Generador de Códigos de Barra",
                     font=ctk.CTkFont("Segoe UI", 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Registre y genere identificadores para el personal",
                     font=ctk.CTkFont("Segoe UI", 11),
                     text_color=COLORS["text_muted"]).pack(anchor="w")

        # ── Formulario ───────────────────────────────────────────────────────
        form = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=14,
                            border_width=1, border_color=COLORS["border"])
        form.pack(fill="x", padx=20, pady=6)

        # Nombre
        ctk.CTkLabel(form, text="Apellidos y Nombres",
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=COLORS["text_muted"], anchor="w").pack(padx=24, pady=(20, 4), fill="x")
        self.name_entry = ctk.CTkEntry(
            form, placeholder_text="Ej: García López, Juan Carlos",
            height=44, corner_radius=10,
            fg_color=COLORS["bg3"], border_color=COLORS["border"],
            text_color=COLORS["text"], font=ctk.CTkFont("Segoe UI", 12)
        )
        self.name_entry.pack(padx=24, pady=(0, 14), fill="x")

        # Tipo de persona
        ctk.CTkLabel(form, text="Tipo de Persona",
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=COLORS["text_muted"], anchor="w").pack(padx=24, fill="x")

        self.type_var = ctk.StringVar(value="Estudiante")
        type_row = ctk.CTkFrame(form, fg_color="transparent")
        type_row.pack(padx=24, pady=(6, 20), fill="x")

        ctk.CTkRadioButton(type_row, text="Estudiante", variable=self.type_var,
                           value="Estudiante",
                           font=ctk.CTkFont("Segoe UI", 12),
                           text_color=COLORS["text"],
                           fg_color=COLORS["accent"]).pack(side="left", padx=(0, 20))
        ctk.CTkRadioButton(type_row, text="Docente", variable=self.type_var,
                           value="Docente",
                           font=ctk.CTkFont("Segoe UI", 12),
                           text_color=COLORS["text"],
                           fg_color=COLORS["accent"]).pack(side="left")

        # Botón generar
        ctk.CTkButton(
            form, text="⊕  Generar y Registrar Código", height=44,
            corner_radius=10, font=ctk.CTkFont("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self.generate_barcode
        ).pack(padx=24, pady=(0, 20), fill="x")

        # ── Vista previa del código ──────────────────────────────────────────
        preview = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=14,
                               border_width=1, border_color=COLORS["border"])
        preview.pack(fill="both", expand=True, padx=20, pady=(6, 20))

        ctk.CTkLabel(preview, text="Vista previa del código",
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=COLORS["text_muted"]).pack(pady=(16, 6))

        sep = ctk.CTkFrame(preview, height=1, fg_color=COLORS["border"])
        sep.pack(fill="x", padx=24, pady=(0, 14))

        self.barcode_label = ctk.CTkLabel(preview, text="El código generado aparecerá aquí",
                                          font=ctk.CTkFont("Segoe UI", 11),
                                          text_color=COLORS["text_muted"])
        self.barcode_label.pack(expand=True)

        # Botón imprimir
        ctk.CTkButton(
            preview, text="🖨  Imprimir Código", height=40,
            corner_radius=10, font=ctk.CTkFont("Segoe UI", 12),
            fg_color=COLORS["bg3"], hover_color=COLORS["border"],
            border_width=1, border_color=COLORS["border"],
            command=self.print_barcode
        ).pack(padx=24, pady=(0, 18), fill="x")

    def generate_barcode(self):
        name = self.name_entry.get().strip()
        person_type = self.type_var.get()

        if not name:
            messagebox.showwarning("Atención", "Ingrese un nombre completo.")
            return

        unique_id = hashlib.md5(name.encode()).hexdigest()

        try:
            conn = db_pool.get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO personas (nombre_completo, codigo_barras, tipo_persona) VALUES (%s, %s, %s)",
                (name, unique_id, person_type)
            )
            conn.commit()

            if person_type == "Estudiante":
                cur.execute("INSERT INTO estudiantes (nombre, codigo_barras) VALUES (%s, %s)", (name, unique_id))
            elif person_type == "Docente":
                cur.execute("INSERT INTO docentes (nombre, codigo_barras) VALUES (%s, %s)", (name, unique_id))

            conn.commit()
            cur.close()
            db_pool.put_conn(conn)

            # Generar imagen del código
            barcode_obj = barcode.get_barcode_class('code128')(unique_id, writer=ImageWriter())
            self.barcode_image = barcode_obj.render()

            # Mostrar en la UI
            preview_img = self.barcode_image.copy()
            preview_img.thumbnail((360, 120))
            tk_img = ImageTk.PhotoImage(preview_img)
            self.barcode_label.configure(image=tk_img, text="")
            self.barcode_label.image = tk_img

            messagebox.showinfo("Éxito", f"'{name}' registrado correctamente como {person_type}.")

        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    def print_barcode(self):
        if self.barcode_image:
            self.barcode_image.show()
        else:
            messagebox.showwarning("Atención", "Primero genere un código de barra.")


if __name__ == "__main__":
    root = ctk.CTk()
    root.configure(fg_color=COLORS["bg"])
    root.geometry("560x620")
    app = GeneradorCodigo(root)
    app.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()





