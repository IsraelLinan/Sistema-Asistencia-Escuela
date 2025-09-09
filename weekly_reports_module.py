# weekly_reports_module.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from colegio_lib import db_pool
from datetime import datetime, timedelta
import csv
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import openpyxl

class WeeklyReportsModule(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Módulo Reporte de Asistencias")
        self.style = ttk.Style()
        self.style.theme_use('plastik')
        self.report_data = []
        self.create_widgets()

    def create_widgets(self):
        # Cargar y mostrar la imagen del logo
        logo_path = "logo_colegio.png"
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((100, 100), Image.Resampling.LANCZOS)
            logo_image = ImageTk.PhotoImage(logo)
            logo_label = ttk.Label(self, image=logo_image)
            logo_label.image = logo_image
            logo_label.grid(row=0, column=0, columnspan=4, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró la imagen del logo.")
            logo_label = ttk.Label(self, text="Logo")
            logo_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Controles de fecha
        ttk.Label(self, text="Fecha Inicio:").grid(row=1, column=0, sticky="W", padx=5, pady=5)
        self.start_date_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Fecha Fin:").grid(row=1, column=2, sticky="W", padx=5, pady=5)
        self.end_date_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date_entry.grid(row=1, column=3, padx=5, pady=5)

        # Filtro por tipo de persona
        ttk.Label(self, text="Tipo:").grid(row=2, column=0, sticky="W", padx=5, pady=5)
        self.type_combobox = ttk.Combobox(self, values=["Todos", "Estudiantes", "Docentes"], state="readonly")
        self.type_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.type_combobox.set("Todos")

        # Botón para cargar el reporte
        self.load_report_btn = ttk.Button(self, text="Cargar Reporte", command=self.load_report_data)
        self.load_report_btn.grid(row=2, column=2, columnspan=2, pady=10)

        # Campo de búsqueda
        ttk.Label(self, text="Buscar:").grid(row=3, column=0, sticky="W", padx=5, pady=5)
        self.search_entry = ttk.Entry(self, width=20)
        self.search_entry.grid(row=3, column=1, columnspan=3, sticky="WE", padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_report)

        # Configuración del Treeview
        columns = ("Tipo", "Nombre", "Hora Ingreso", "Hora Salida")
        self.report_tree = ttk.Treeview(self, columns=columns, show="headings")
        self.report_tree.heading("Tipo", text="Tipo")
        self.report_tree.heading("Nombre", text="Nombre")
        self.report_tree.heading("Hora Ingreso", text="Hora Ingreso")
        self.report_tree.heading("Hora Salida", text="Hora Salida") # Nueva columna
        self.report_tree.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Ajuste de las columnas
        self.report_tree.column("Tipo", width=100)
        self.report_tree.column("Nombre", width=200)
        self.report_tree.column("Hora Ingreso", width=120)
        self.report_tree.column("Hora Salida", width=120) # Ancho de la nueva columna

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.report_tree.yview)
        scrollbar.grid(row=4, column=4, sticky="ns")
        self.report_tree.configure(yscrollcommand=scrollbar.set)

        # Botones de exportación
        self.export_csv_btn = ttk.Button(self, text="Exportar a CSV", command=self.export_to_csv)
        self.export_csv_btn.grid(row=5, column=0, padx=5, pady=10)
        self.export_pdf_btn = ttk.Button(self, text="Exportar a PDF", command=self.export_to_pdf)
        self.export_pdf_btn.grid(row=5, column=1, padx=5, pady=10)
        self.export_xlsx_btn = ttk.Button(self, text="Exportar a XLSX", command=self.export_to_xlsx)
        self.export_xlsx_btn.grid(row=5, column=2, padx=5, pady=10)

    def load_report_data(self):
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        person_type = self.type_combobox.get()
        self.report_data = []
        conn = None
        try:
            conn = db_pool.get_conn()
            cur = conn.cursor()

            # Lógica para Estudiantes
            if person_type in ["Todos", "Estudiante"]:
                cur.execute(
                    "SELECT 'Estudiante', e.nombre, i.hora_ingreso, NULL FROM ingresos_estudiantes i JOIN estudiantes e ON i.estudiante_id = e.id WHERE DATE(i.hora_ingreso) BETWEEN %s AND %s ORDER BY i.hora_ingreso",
                    (start_date, end_date)
                )
                student_records = cur.fetchall()
                for rec in student_records:
                    self.report_data.append({
                        'tipo': rec[0],
                        'nombre': rec[1],
                        'hora_ingreso': rec[2].strftime('%Y-%m-%d %H:%M:%S'),
                        'hora_salida': 'N/A' # Estudiantes no tienen hora de salida en esta tabla
                    })

            # Lógica para Docentes
            if person_type in ["Todos", "Docente"]:
                # Se selecciona hora_salida, que puede ser nula
                cur.execute(
                    "SELECT 'Docente', d.nombre, i.hora_ingreso, i.hora_salida FROM ingresos_docentes i JOIN docentes d ON i.docente_id = d.id WHERE DATE(i.hora_ingreso) BETWEEN %s AND %s ORDER BY i.hora_ingreso",
                    (start_date, end_date)
                )
                teacher_records = cur.fetchall()
                for rec in teacher_records:
                    hora_salida = rec[3].strftime('%Y-%m-%d %H:%M:%S') if rec[3] else 'No registrada'
                    self.report_data.append({
                        'tipo': rec[0],
                        'nombre': rec[1],
                        'hora_ingreso': rec[2].strftime('%Y-%m-%d %H:%M:%S'),
                        'hora_salida': hora_salida
                    })

            cur.close()
            self.refresh_treeview()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el reporte: {e}")
        finally:
            if conn:
                db_pool.put_conn(conn)

    def refresh_treeview(self):
        # Limpiar Treeview
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        # Insertar datos filtrados
        for record in self.report_data:
            self.report_tree.insert("", "end", values=(
                record['tipo'],
                record['nombre'],
                record['hora_ingreso'],
                record['hora_salida']
            ))

    def filter_report(self, event=None):
        query = self.search_entry.get().lower()
        
        # Limpiar Treeview
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        # Insertar solo los registros que coinciden con la búsqueda
        for record in self.report_data:
            if query in record['nombre'].lower() or query in record['tipo'].lower():
                self.report_tree.insert("", "end", values=(
                    record['tipo'],
                    record['nombre'],
                    record['hora_ingreso'],
                    record['hora_salida']
                ))

    def export_to_csv(self):
        if not self.report_data:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return
        
        default_filename = f"Reporte de Asistencia_{datetime.now().strftime('%Y-%m-%d')}.csv"

        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],initialfile=default_filename)
        if not filepath:
            return
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['tipo', 'nombre', 'hora_ingreso', 'hora_salida']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for record in self.report_data:
                    writer.writerow(record)
            messagebox.showinfo("Éxito", f"Reporte CSV guardado en {filepath}")
        except Exception as e:
            messagebox.showerror("Error CSV", str(e))

    def export_to_pdf(self):
        if not self.report_data:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return
        
        default_filename = f"Reporte de Asistencia_{datetime.now().strftime('%Y-%m-%d')}.pdf"

        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],initialfile=default_filename)
        if filepath:
            c = canvas.Canvas(filepath, pagesize=letter)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, 750, "Reporte de Asistencia")
            c.line(30, 745, 580, 745)

            y_pos = 720
            c.setFont("Helvetica-Bold", 10)
            c.drawString(40, y_pos, "Tipo")
            c.drawString(140, y_pos, "Nombre")
            c.drawString(340, y_pos, "Hora Ingreso")
            c.drawString(470, y_pos, "Hora Salida") # Nueva columna

            y_pos -= 20
            c.setFont("Helvetica", 9)
            for record in self.report_data:
                if y_pos < 50:
                    c.showPage()
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(40, 750, "Tipo")
                    c.drawString(140, 750, "Nombre")
                    c.drawString(340, 750, "Hora Ingreso")
                    c.drawString(470, 750, "Hora Salida") # Nueva columna
                    y_pos = 730
                    c.setFont("Helvetica", 9)
                
                c.drawString(40, y_pos, record['tipo'])
                c.drawString(140, y_pos, record['nombre'])
                c.drawString(340, y_pos, record['hora_ingreso'])
                c.drawString(470, y_pos, record['hora_salida'])
                y_pos -= 15
            
            c.save()
            messagebox.showinfo("Éxito", f"Reporte PDF guardado en:\n{filepath}")

    def export_to_xlsx(self):
        if not self.report_data:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return
        
        default_filename = f"Reporte de Asistencia_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")],initialfile=default_filename)
        if filepath:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Reporte de Asistencia"

            # Encabezados
            headers = ["Tipo", "Nombre", "Hora Ingreso", "Hora Salida"]
            ws.append(headers)

            # Ajuste de estilos de encabezados
            header_font = openpyxl.styles.Font(bold=True)
            header_fill = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
            for col_num, cell in enumerate(ws[1], 1):
                cell.font = header_font
                cell.fill = header_fill
                ws.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = 25

            # Agregar los datos
            for record in self.report_data:
                ws.append([
                    record['tipo'],
                    record['nombre'],
                    record['hora_ingreso'],
                    record['hora_salida']
                ])

            wb.save(filepath)
            messagebox.showinfo("Éxito", f"Reporte XLSX guardado en:\n{filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyReportsModule(root)
    app.pack(fill='both', expand=True, padx=10, pady=10)
    root.mainloop()













