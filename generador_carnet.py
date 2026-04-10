import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageOps
import hashlib
import os
import math
import io

def _generate_barcode_image(code, width=400, height=80):
    """
    Genera una imagen PIL de código de barras Code128 usando python-barcode.
    Si no está disponible, genera barras usando PIL puro como fallback.
    """
    try:
        import barcode
        from barcode.writer import ImageWriter
        import io
        bc_class = barcode.get_barcode_class('code128')
        writer = ImageWriter()
        writer.set_options({
            'module_width': 0.8,
            'module_height': 8,
            'font_size': 6,
            'text_distance': 3,
            'quiet_zone': 3,
            'background': 'white',
            'foreground': 'black',
        })
        bc = bc_class(code, writer=writer)
        buf = io.BytesIO()
        bc.write(buf)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((width, height), Image.LANCZOS)
        return img
    except ImportError:
        # Fallback: barras verticales simples representando el código
        img = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Patrón basado en los bytes del código
        bar_w = max(1, width // (len(code) * 8))
        x = 4
        for char in code:
            bits = format(ord(char), '08b')
            for bit in bits:
                if bit == '1':
                    draw.rectangle([x, 4, x + bar_w, height - 14], fill=(0, 0, 0))
                x += bar_w + 1
                if x >= width - 4:
                    break
        # Texto del código debajo
        try:
            font = ImageFont.truetype(FONT_REGULAR, 9)
        except Exception:
            font = ImageFont.load_default()
        draw.text((width // 2, height - 12), code, font=font,
                  fill=(0, 0, 0), anchor='mm' if hasattr(font, 'getlength') else None)
        return img
from datetime import datetime
from colegio_lib import db_pool, COLORS

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Rutas de fuentes ─────────────────────────────────────────────────────────
FONT_BOLD    = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FONT_MEDIUM  = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"

# Fallback a DejaVu si no existe Poppins (Windows usará sus propias fuentes)
if not os.path.exists(FONT_BOLD):
    FONT_BOLD    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    FONT_MEDIUM  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# En Windows buscar fuentes del sistema
def _win_font(name):
    paths = [
        f"C:/Windows/Fonts/{name}",
        os.path.join(os.environ.get("WINDIR", ""), f"Fonts/{name}")
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

if os.name == "nt":
    FONT_BOLD    = _win_font("arialbd.ttf")   or FONT_BOLD
    FONT_MEDIUM  = _win_font("arial.ttf")     or FONT_MEDIUM
    FONT_REGULAR = _win_font("arial.ttf")     or FONT_REGULAR


# ════════════════════════════════════════════════════════════════════════════
#  GENERADOR DE IMAGEN DEL CARNÉ
# ════════════════════════════════════════════════════════════════════════════

def generate_carnet_image(nombre, grado, anio, foto_path=None,
                           institucion="INSTITUCIÓN EDUCATIVA",
                           logo_path="logo_colegio.png"):
    """
    Genera la imagen del carné de estudiante (1011 x 639 px).
    Devuelve un objeto PIL.Image.
    """
    W, H = 1011, 639

    # ── Lienzo base blanco ───────────────────────────────────────────────────
    card = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(card)

    # ── Franja superior (fondo degradado simulado con polígonos) ────────────
    HEADER_H = 280

    # Fondo base azul oscuro
    draw.rectangle([(0, 0), (W, HEADER_H)], fill=(22, 57, 120))

    # Patrón geométrico tipo low-poly (triángulos decorativos)
    triangles = [
        # Zona izquierda — verdes/cyan
        [(0, 0),    (180, 0),   (90, 120),    (0, 90, 140, 70)],
        [(0, 0),    (90, 120),  (0, 200),     (0, 130, 100, 80)],
        [(180, 0),  (320, 0),   (200, 160),   (0, 150, 120, 90)],
        [(90, 120), (200, 160), (0, 200),     (20, 120, 100, 100)],
        [(0, 200),  (200, 160), (0, HEADER_H),(0, 100, 80, 110)],
        [(200, 160),(300, HEADER_H),(0, HEADER_H),(30, 90, 70, 120)],
        # Zona derecha — azules variados
        [(W, 0),    (W-200, 0), (W-100, 130), (30, 60, 140, 80)],
        [(W, 0),    (W-100, 130),(W, 180),    (20, 50, 130, 90)],
        [(W-200, 0),(W-350, 0), (W-250, 150), (25, 70, 150, 70)],
        [(W-100, 130),(W-250, 150),(W, 180),  (15, 45, 120, 100)],
        [(W, 180),  (W-250, 150),(W, HEADER_H),(10, 40, 110, 110)],
        [(W-250,150),(W-300,HEADER_H),(W,HEADER_H),(20,55,130,90)],
        # Centro — azul medio
        [(320, 0),  (W-350, 0), (W-250, 150), (25, 65, 145, 80)],
        [(320, 0),  (W-250,150),(300, HEADER_H),(20,60,140,90)],
    ]
    for tri in triangles:
        pts = [tri[0], tri[1], tri[2]]
        r, g, b, a = tri[3]
        # Mezclar con el fondo azul oscuro
        color = (min(255, 22+r), min(255, 57+g), min(255, 120+b))
        draw.polygon(pts, fill=color)

    # ── Franja inferior verde ────────────────────────────────────────────────
    FOOTER_H = 55
    draw.rectangle([(0, H - FOOTER_H), (W, H)], fill=(58, 180, 100))

    # Triángulos decorativos en el footer
    footer_tris = [
        [(0, H-FOOTER_H), (150, H-FOOTER_H), (0, H), (0, 140, 70)],
        [(150, H-FOOTER_H),(300, H-FOOTER_H),(200, H),(0, 160, 80)],
        [(W, H-FOOTER_H), (W-180, H-FOOTER_H),(W, H),(0, 120, 60)],
        [(W-180, H-FOOTER_H),(W-320,H-FOOTER_H),(W-200,H),(0,150,75)],
    ]
    for tri in footer_tris:
        pts = [tri[0], tri[1], tri[2]]
        r, g, b = tri[3]
        color = (min(255, 58+r), min(255, 180+g), min(255, 100+b))
        draw.polygon(pts, fill=color)

    # ── Zona blanca central (debajo del header) ──────────────────────────────
    # Ya es blanco por defecto

    # ── Círculo de foto ──────────────────────────────────────────────────────
    CX, CY = 210, 245   # centro del círculo
    CR = 155            # radio

    # Sombra suave
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    for i in range(8, 0, -1):
        sdraw.ellipse(
            [CX - CR - i*2, CY - CR - i*2, CX + CR + i*2, CY + CR + i*2],
            fill=(0, 0, 0, 10)
        )
    card.paste(Image.alpha_composite(
        Image.new("RGBA", (W, H), (0, 0, 0, 0)), shadow
    ).convert("RGB"), mask=shadow.split()[3])

    # Borde blanco grueso
    draw.ellipse(
        [CX - CR - 12, CY - CR - 12, CX + CR + 12, CY + CR + 12],
        fill=(255, 255, 255)
    )

    # Foto o placeholder
    if foto_path and os.path.exists(foto_path):
        try:
            foto = Image.open(foto_path).convert("RGB")
            foto = foto.resize((CR * 2, CR * 2), Image.LANCZOS)
        except Exception:
            foto = _placeholder_photo(CR * 2)
    else:
        foto = _placeholder_photo(CR * 2)

    # Recorte circular de la foto
    mask_circle = Image.new("L", (CR * 2, CR * 2), 0)
    ImageDraw.Draw(mask_circle).ellipse([0, 0, CR * 2, CR * 2], fill=255)
    foto_round = Image.new("RGB", (CR * 2, CR * 2), (255, 255, 255))
    foto_round.paste(foto, mask=mask_circle)

    card.paste(foto_round, (CX - CR, CY - CR), mask=mask_circle)

    # ── Logo institucional (encima del nombre de la institución) ────────────
    LOGO_SIZE = 70
    LOGO_X    = 420   # mismo X que el texto de institución
    LOGO_Y    = 14    # margen superior dentro del header
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
        card.paste(logo, (LOGO_X, LOGO_Y), mask=logo.split()[3])
    except Exception:
        pass
    # El texto de institución comenzará justo debajo del logo
    INST_Y = LOGO_Y + LOGO_SIZE + 6

    # ── Textos del header ────────────────────────────────────────────────────
    try:
        font_inst   = ImageFont.truetype(FONT_BOLD,    22)
        font_title  = ImageFont.truetype(FONT_BOLD,    54)
        font_label  = ImageFont.truetype(FONT_MEDIUM,  28)
        font_value  = ImageFont.truetype(FONT_BOLD,    28)
        font_small  = ImageFont.truetype(FONT_REGULAR, 20)
    except Exception:
        font_inst  = ImageFont.load_default()
        font_title = font_inst
        font_label = font_inst
        font_value = font_inst
        font_small = font_inst

    # Nombre institución (debajo del logo)
    draw.text((420, INST_Y), institucion.upper(),
              font=font_inst, fill=(180, 220, 255))

    # Título "Carné de Estudiante" (debajo del nombre institución)
    draw.text((420, INST_Y + 30), "Carné de Estudiante",
              font=font_title, fill=(255, 255, 255))

    # ── Datos del estudiante (zona blanca) ───────────────────────────────────
    DATA_X_LABEL = 420
    DATA_X_VALUE = 590
    DATA_Y_START = 320
    LINE_H       = 52

    campos = [
        ("Nombre",  nombre),
        ("Grado",   grado),
        ("Año",     str(anio)),
    ]

    for i, (label, value) in enumerate(campos):
        y = DATA_Y_START + i * LINE_H
        draw.text((DATA_X_LABEL, y), f"{label}", font=font_label, fill=(80, 80, 80))
        draw.text((DATA_X_LABEL + 130, y), ":", font=font_label, fill=(80, 80, 80))
        draw.text((DATA_X_VALUE, y), value, font=font_value, fill=(30, 30, 30))

    # ── Código de barras real (escaneable con pistola lectora) ─────────────
    # Buscar el código real del estudiante en la BD o generar uno basado en MD5
    code = hashlib.md5(nombre.encode()).hexdigest()[:16].upper()
    
    # Intentar obtener el código real de la BD si db_pool está disponible
    try:
        from colegio_lib import db_pool as _pool
        if _pool is not None:
            _conn = _pool.get_conn()
            _cur = _conn.cursor()
            _cur.execute(
                "SELECT codigo_barras FROM estudiantes WHERE LOWER(nombre) = LOWER(%s) LIMIT 1",
                (nombre,)
            )
            _row = _cur.fetchone()
            if _row:
                code = _row[0]
            _cur.close()
            _pool.put_conn(_conn)
    except Exception:
        pass  # Usar el código MD5 como fallback

    # Generar imagen del código de barras
    barcode_img = _generate_barcode_image(code, width=380, height=72)
    
    # Pegar en el carné
    bc_x = 415
    bc_y = DATA_Y_START + 3 * LINE_H + 8
    card.paste(barcode_img, (bc_x, bc_y))

    # ── Línea separadora entre foto y datos ──────────────────────────────────
    draw.line([(390, 310), (390, 580)], fill=(220, 220, 220), width=2)

    return card


def _placeholder_photo(size):
    """Genera una foto placeholder con fondo degradado y silueta."""
    img = Image.new("RGB", (size, size), (135, 200, 220))
    draw = ImageDraw.Draw(img)

    # Cielo
    for y in range(size):
        ratio = y / size
        r = int(135 + (200 - 135) * ratio)
        g = int(200 + (230 - 200) * ratio)
        b = int(220 + (240 - 220) * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b))

    # Nube
    cx, cy = size // 2, size // 3
    for dx, dy, r in [(0, 0, 30), (-28, 10, 22), (28, 10, 22), (-14, 18, 18), (14, 18, 18)]:
        draw.ellipse([cx+dx-r, cy+dy-r, cx+dx+r, cy+dy+r], fill=(255, 255, 255))

    # Colina verde
    hill_y = int(size * 0.62)
    draw.ellipse([-size//3, hill_y, size + size//3, size + size//2],
                 fill=(100, 180, 60))
    draw.ellipse([size//4, hill_y + 20, size + size//4, size + size//2 + 20],
                 fill=(80, 160, 50))

    return img


# ════════════════════════════════════════════════════════════════════════════
#  MÓDULO CTK
# ════════════════════════════════════════════════════════════════════════════

class GeneradorCarnet(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.parent = parent
        if isinstance(parent, (ctk.CTk, ctk.CTkToplevel)):
            self.parent.title("Generador de Carné Estudiantil")
        self.foto_path = None
        self.carnet_img = None
        self._build_ui()

    def _build_ui(self):
        # ── Layout principal: izquierda (formulario) | derecha (preview) ────
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ════ PANEL IZQUIERDO — Formulario ════
        left = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=14,
                            border_width=1, border_color=COLORS["border"])
        left.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)

        # Encabezado
        ctk.CTkLabel(left, text="🪪  Datos del Carné",
                     font=ctk.CTkFont("Segoe UI", 15, "bold"),
                     text_color=COLORS["text"]).pack(pady=(20, 4), padx=20, anchor="w")
        ctk.CTkLabel(left, text="Complete los campos y genere el carné",
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=COLORS["text_muted"]).pack(padx=20, anchor="w")

        ctk.CTkFrame(left, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=12)

        # ── Campo: Institución ──
        self._field(left, "Institución Educativa")
        self.inst_entry = self._entry(left, "Nombre del colegio")

        # ── Campo: Nombre del estudiante (con autocompletado desde BD) ──
        self._field(left, "Nombre del Estudiante")
        self.nombre_entry = self._entry(left, "Buscar o escribir nombre...")
        self.nombre_entry.bind("<KeyRelease>", self._on_nombre_key)

        # Lista de sugerencias
        self.suggest_frame = ctk.CTkFrame(left, fg_color=COLORS["bg3"],
                                          corner_radius=8, border_width=1,
                                          border_color=COLORS["border"])
        self.suggest_frame.pack(fill="x", padx=20, pady=(0, 4))
        self.suggest_frame.pack_forget()

        # ── Campo: Grado ──
        self._field(left, "Grado / Sección")
        self.grado_entry = self._entry(left, "Ej: 3° Secundaria A")

        # ── Campo: Año ──
        self._field(left, "Año Lectivo")
        self.anio_entry = self._entry(left, str(datetime.now().year))
        self.anio_entry.insert(0, str(datetime.now().year))

        # ── Foto del estudiante ──
        ctk.CTkFrame(left, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=12)
        self._field(left, "Foto del Estudiante  (opcional)")

        foto_row = ctk.CTkFrame(left, fg_color="transparent")
        foto_row.pack(fill="x", padx=20, pady=(4, 0))

        self.foto_label = ctk.CTkLabel(foto_row, text="Sin foto seleccionada",
                                        font=ctk.CTkFont("Segoe UI", 10),
                                        text_color=COLORS["text_muted"])
        self.foto_label.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(foto_row, text="📁", width=38, height=32,
                      corner_radius=8,
                      fg_color=COLORS["bg3"], hover_color=COLORS["border"],
                      command=self._select_foto).pack(side="right")

        # Vista previa de la foto seleccionada
        self.foto_preview = ctk.CTkLabel(left, text="", width=80, height=80)
        self.foto_preview.pack(pady=(8, 0))

        # ── Botón generar ──
        ctk.CTkFrame(left, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=14)

        ctk.CTkButton(left, text="⊕  Generar Carné", height=44,
                      corner_radius=10,
                      font=ctk.CTkFont("Segoe UI", 13, "bold"),
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                      command=self._generate).pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkButton(left, text="💾  Guardar como imagen", height=38,
                      corner_radius=10,
                      font=ctk.CTkFont("Segoe UI", 11),
                      fg_color=COLORS["bg3"], hover_color=COLORS["border"],
                      border_width=1, border_color=COLORS["border"],
                      command=self._save).pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkButton(left, text="🖨  Imprimir", height=38,
                      corner_radius=10,
                      font=ctk.CTkFont("Segoe UI", 11),
                      fg_color=COLORS["bg3"], hover_color=COLORS["border"],
                      border_width=1, border_color=COLORS["border"],
                      command=self._print).pack(fill="x", padx=20, pady=(0, 20))

        # ════ PANEL DERECHO — Vista previa ════
        right = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=14,
                             border_width=1, border_color=COLORS["border"])
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)

        ctk.CTkLabel(right, text="Vista Previa del Carné",
                     font=ctk.CTkFont("Segoe UI", 13, "bold"),
                     text_color=COLORS["text_muted"]).pack(pady=(18, 8))

        ctk.CTkFrame(right, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=(0, 16))

        # Contenedor del carné
        self.preview_container = ctk.CTkFrame(right, fg_color=COLORS["bg3"],
                                              corner_radius=12)
        self.preview_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.preview_label = ctk.CTkLabel(
            self.preview_container,
            text="El carné aparecerá aquí\ndespués de generarlo",
            font=ctk.CTkFont("Segoe UI", 13),
            text_color=COLORS["text_muted"]
        )
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

    def _field(self, parent, text):
        ctk.CTkLabel(parent, text=text,
                     font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=COLORS["text_muted"],
                     anchor="w").pack(padx=20, pady=(10, 2), fill="x")

    def _entry(self, parent, placeholder):
        e = ctk.CTkEntry(parent, placeholder_text=placeholder,
                         height=38, corner_radius=8,
                         fg_color=COLORS["bg3"], border_color=COLORS["border"],
                         text_color=COLORS["text"],
                         font=ctk.CTkFont("Segoe UI", 12))
        e.pack(padx=20, pady=(0, 2), fill="x")
        return e

    # ── Autocompletado desde la BD ───────────────────────────────────────────
    def _on_nombre_key(self, event=None):
        query = self.nombre_entry.get().strip()
        for w in self.suggest_frame.winfo_children():
            w.destroy()

        if len(query) < 2:
            self.suggest_frame.pack_forget()
            return

        try:
            conn = db_pool.get_conn()
            cur = conn.cursor()
            cur.execute(
                "SELECT nombre FROM estudiantes WHERE LOWER(nombre) LIKE LOWER(%s) LIMIT 6",
                (f"%{query}%",)
            )
            results = [r[0] for r in cur.fetchall()]
            cur.close()
            db_pool.put_conn(conn)
        except Exception:
            results = []

        if not results:
            self.suggest_frame.pack_forget()
            return

        self.suggest_frame.pack(fill="x", padx=20, pady=(0, 4))
        for name in results:
            btn = ctk.CTkButton(
                self.suggest_frame, text=name, anchor="w",
                height=32, corner_radius=6,
                fg_color="transparent", hover_color=COLORS["border"],
                text_color=COLORS["text"], font=ctk.CTkFont("Segoe UI", 11),
                command=lambda n=name: self._select_nombre(n)
            )
            btn.pack(fill="x", padx=4, pady=1)

    def _select_nombre(self, nombre):
        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, nombre)
        self.suggest_frame.pack_forget()

    # ── Selección de foto ────────────────────────────────────────────────────
    def _select_foto(self):
        path = filedialog.askopenfilename(
            title="Seleccionar foto del estudiante",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.foto_path = path
            fname = os.path.basename(path)
            self.foto_label.configure(
                text=fname[:28] + "..." if len(fname) > 28 else fname,
                text_color=COLORS["success"]
            )
            # Miniatura de la foto
            try:
                thumb = Image.open(path).convert("RGB")
                thumb.thumbnail((70, 70))
                tk_thumb = ctk.CTkImage(light_image=thumb, dark_image=thumb, size=(70, 70))
                self.foto_preview.configure(image=tk_thumb, text="")
                self.foto_preview.image = tk_thumb
            except Exception:
                pass

    # ── Generar carné ────────────────────────────────────────────────────────
    def _generate(self):
        nombre = self.nombre_entry.get().strip()
        grado  = self.grado_entry.get().strip()
        anio   = self.anio_entry.get().strip()
        inst   = self.inst_entry.get().strip() or "INSTITUCIÓN EDUCATIVA"

        if not nombre:
            messagebox.showwarning("Atención", "Ingrese el nombre del estudiante.")
            return
        if not grado:
            messagebox.showwarning("Atención", "Ingrese el grado del estudiante.")
            return
        if not anio:
            anio = str(datetime.now().year)

        try:
            self.carnet_img = generate_carnet_image(
                nombre=nombre,
                grado=grado,
                anio=anio,
                foto_path=self.foto_path,
                institucion=inst,
                logo_path="logo_colegio.png"
            )
            self._update_preview()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el carné:\n{e}")

    def _update_preview(self):
        if not self.carnet_img:
            return
        # Escalar para que quepa en el panel de preview
        self.preview_container.update_idletasks()
        pw = self.preview_container.winfo_width() - 40
        ph = self.preview_container.winfo_height() - 40
        if pw < 100 or ph < 100:
            pw, ph = 600, 380

        img_copy = self.carnet_img.copy()
        img_copy.thumbnail((pw, ph), Image.LANCZOS)

        tk_img = ctk.CTkImage(
            light_image=img_copy,
            dark_image=img_copy,
            size=img_copy.size
        )
        self.preview_label.configure(image=tk_img, text="")
        self.preview_label.image = tk_img

    # ── Guardar imagen ───────────────────────────────────────────────────────
    def _save(self):
        if not self.carnet_img:
            messagebox.showwarning("Atención", "Primero genere el carné.")
            return
        nombre = self.nombre_entry.get().strip().replace(" ", "_") or "carnet"
        default = f"Carnet_{nombre}_{datetime.now().strftime('%Y%m%d')}.png"
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
            initialfile=default
        )
        if path:
            self.carnet_img.save(path, quality=95)
            messagebox.showinfo("Éxito", f"Carné guardado en:\n{path}")

    # ── Imprimir ─────────────────────────────────────────────────────────────
    def _print(self):
        if not self.carnet_img:
            messagebox.showwarning("Atención", "Primero genere el carné.")
            return
        self.carnet_img.show()


# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = ctk.CTk()
    root.configure(fg_color=COLORS["bg"])
    root.geometry("1100x680")
    root.title("Generador de Carné Estudiantil")
    app = GeneradorCarnet(root)
    app.pack(fill="both", expand=True)
    root.mainloop()