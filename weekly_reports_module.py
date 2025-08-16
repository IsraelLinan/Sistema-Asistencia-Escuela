import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from colegio_lib import db_pool  # Importamos el pool de conexiones
from datetime import datetime, timedelta
import csv
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import openpyxl  # Librería para manejar archivos Excel

class WeeklyReportsModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Módulo Reporte de Asistencias")
        self.style = ttk.Style()
        self.style.theme_use('plastik')  # Aplicamos el tema 'plastik'
        self.report_data = []
        self.create_widgets()

    def create_widgets(self):
        # Cargar y mostrar la imagen del logo
        logo_path = "logo_colegio.png"  # Ruta de la imagen
        logo = Image.open(logo_path)  # Abrir la imagen
        logo = logo.resize((100, 100), Image.Resampling.LANCZOS)  # Ajustar el tamaño de la imagen
        logo_image = ImageTk.PhotoImage(logo)  # Convertir la imagen a un formato que Tkinter pueda usar

        logo_label = ttk.Label(self, image=logo_image)
        logo_label.image = logo_image  # Guardar una referencia a la imagen
        logo_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Etiquetas y campos de fecha con calendario y filtro, alineados en una cuadrícula
        ttk.Label(self, text="Fecha Inicio:").grid(row=1, column=0, sticky="W", padx=5, pady=5)
        ttk.Label(self, text="Fecha Fin:").grid(row=2, column=0, sticky="W", padx=5, pady=5)
        ttk.Label(self, text="Filtro:").grid(row=3, column=0, sticky="W", padx=5, pady=5)

        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        self.start_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_entry.set_date(week_ago)
        self.start_entry.grid(row=1, column=1, pady=5, sticky="W")

        self.end_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_entry.set_date(today)
        self.end_entry.grid(row=2, column=1, pady=5, sticky="W")

        self.filter_combo = ttk.Combobox(self, values=["Todos", "Estudiante", "Docente"], state='readonly', width=10)
        self.filter_combo.current(0)
        self.filter_combo.grid(row=3, column=1, pady=5, sticky="W")

        # Campo de búsqueda
        ttk.Label(self, text="Buscar por nombre:").grid(row=4, column=0, sticky="W", padx=5, pady=5)
        self.search_entry = ttk.Entry(self, width=30)
        self.search_entry.grid(row=4, column=1, pady=5, sticky="W")
        self.search_entry.bind("<KeyRelease>", self.search)  # Asociamos la función de búsqueda

        # Botón para cargar reporte
        self.load_btn = ttk.Button(self, text="Cargar Reporte", command=self.load_report)
        self.load_btn.grid(row=5, column=2, pady=10, padx=(10,0))

        # Treeview para mostrar datos
        columns = ("tipo", "nombre", "hora_ingreso")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        for col, text, width in [
            ("tipo", "Tipo", 100),
            ("nombre", "Nombre", 200),
            ("hora_ingreso", "Hora de Ingreso", 150)
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        self.tree.grid(row=6, column=0, columnspan=3, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=3, sticky='ns')

        # Botones de exportación
        self.csv_btn = ttk.Button(self, text="Exportar CSV", command=self.export_csv)
        self.csv_btn.grid(row=7, column=0, pady=10)
        self.pdf_btn = ttk.Button(self, text="Exportar PDF", command=self.export_pdf)
        self.pdf_btn.grid(row=7, column=1, pady=10)
        self.xlsx_btn = ttk.Button(self, text="Exportar XLSX", command=self.export_xlsx)  # Add XLSX export button
        self.xlsx_btn.grid(row=7, column=2, pady=10)

    def search(self, event):
        """Buscar por nombre en el Treeview mientras el usuario escribe"""
        search_term = self.search_entry.get().lower()
        
        # Limpiar los datos previos
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar solo los registros que coincidan con la búsqueda
        filtered_data = [record for record in self.report_data if search_term in record['nombre'].lower()]
        for record in filtered_data:
            self.tree.insert('', 'end', values=(record['tipo'], record['nombre'], record['hora_ingreso']))

    def load_report(self):
        start_dt = datetime.combine(self.start_entry.get_date(), datetime.min.time())
        end_dt = datetime.combine(self.end_entry.get_date() + timedelta(days=1), datetime.min.time())
        filtro = self.filter_combo.get()

        # Limpiar datos previos
        self.report_data.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            # Obtener una conexión del pool
            conn = db_pool.get_conn()
            cur = conn.cursor()

            # Función para consulta genérica
            def fetch(tipo, ingress_table, person_table, id_field):
                query = (
                    f"SELECT p.nombre AS nombre, i.hora_ingreso "
                    f"FROM {ingress_table} i "
                    f"JOIN {person_table} p ON i.{id_field} = p.id "
                    "WHERE i.hora_ingreso >= %s AND i.hora_ingreso < %s "
                    "ORDER BY i.hora_ingreso;"
                )
                cur.execute(query, (start_dt, end_dt))
                for nombre, hora in cur.fetchall():
                    hora_str = hora.strftime('%Y-%m-%d %H:%M:%S')
                    if filtro == 'Todos' or filtro == tipo:
                        self.report_data.append({'tipo': tipo, 'nombre': nombre, 'hora_ingreso': hora_str})

            # Reporte estudiantes y docentes
            fetch('Estudiante', 'ingresos_estudiantes', 'estudiantes', 'estudiante_id')
            fetch('Docente', 'ingresos_docentes', 'docentes', 'docente_id')

            cur.close()
            # Devolver la conexión al pool
            db_pool.put_conn(conn)

            # Mostrar en Treeview
            for record in self.report_data:
                self.tree.insert('', 'end', values=(record['tipo'], record['nombre'], record['hora_ingreso']))
        except Exception as e:
            messagebox.showerror("Error BD", str(e))

    def export_csv(self):
        if not self.report_data:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
        filepath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')], initialfile=filename)
        if not filepath:
            return
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['tipo', 'nombre', 'hora_ingreso']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for record in self.report_data:
                    writer.writerow(record)
            messagebox.showinfo("Éxito", f"Reporte CSV guardado en {filepath}")
        except Exception as e:
            messagebox.showerror("Error CSV", str(e))

    def export_pdf(self):
        if not self.report_data:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return
        # Usar la fecha actual en el nombre del archivo
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"
        filepath = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF files','*.pdf')], initialfile=filename)
        if not filepath:
            return
        try:
            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter  # Dimensiones de la página (8.5 x 11 pulgadas)

            # Títulos y márgenes
            margin_left = 50
            margin_top = 750
            line_height = 15
            title = f"Reporte Semanal de Ingresos - {self.filter_combo.get()}"

            # Encabezado
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin_left, margin_top, title)
            margin_top -= 15  # Espacio para el título

            # Subtítulos para las columnas
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin_left, margin_top, "Tipo")
            c.drawString(margin_left + 150, margin_top, "Nombre")
            c.drawString(margin_left + 350, margin_top, "Hora de Ingreso")
            margin_top -= 15  # Espacio para los encabezados de columna

            # Ingresar los datos
            c.setFont("Helvetica", 10)
            y_position = margin_top
            for record in self.report_data:
                c.drawString(margin_left, y_position, record['tipo'])
                c.drawString(margin_left + 150, y_position, record['nombre'])
                c.drawString(margin_left + 350, y_position, record['hora_ingreso'])
                y_position -= line_height

                # Si se llega al final de la página, crear una nueva página
                if y_position < 50:
                    c.showPage()  # Nueva página
                    c.setFont("Helvetica", 10)  # Resetear la fuente
                    y_position = margin_top  # Volver a la parte superior de la página
                    # Redibujar los encabezados en la nueva página
                    c.drawString(margin_left, y_position, "Tipo")
                    c.drawString(margin_left + 150, y_position, "Nombre")
                    c.drawString(margin_left + 350, y_position, "Hora de Ingreso")
                    y_position -= 5

            c.save()
            messagebox.showinfo("Éxito", f"Reporte PDF guardado en {filepath}")
        except Exception as e:
            messagebox.showerror("Error PDF", str(e))

    def export_xlsx(self):
        if not self.report_data:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"
        filepath = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files','*.xlsx')], initialfile=filename)
        if not filepath:
            return
        try:
            # Crear un libro de trabajo de Excel
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Reporte de Asistencia"

            # Establecer los encabezados en negrita y con color de fondo
            header_font = openpyxl.styles.Font(bold=True)
            header_fill = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

            ws['A1'] = 'Tipo'
            ws['B1'] = 'Nombre'
            ws['C1'] = 'Hora de Ingreso'
            for cell in ['A1', 'B1', 'C1']:
                ws[cell].font = header_font
                ws[cell].fill = header_fill

            # Ajuste automático del ancho de las columnas
            ws.column_dimensions['A'].width = 20
            ws.column_dimensions['B'].width = 30
            ws.column_dimensions['C'].width = 25

            # Agregar los datos a la hoja de trabajo
            row_num = 2
            for record in self.report_data:
                ws[f'A{row_num}'] = record['tipo']
                ws[f'B{row_num}'] = record['nombre']
                ws[f'C{row_num}'] = record['hora_ingreso']
                row_num += 1

            # Guardar el archivo XLSX
            wb.save(filepath)
            messagebox.showinfo("Éxito", f"Reporte XLSX guardado en {filepath}")
        except Exception as e:
            messagebox.showerror("Error XLSX", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyReportsModule(root)
    app.pack(padx=10, pady=10)
    root.mainloop()













