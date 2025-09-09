import streamlit as st
import pandas as pd
from colegio_lib import db_pool
from datetime import datetime
import plotly.express as px

def get_data_for_dashboard(selected_date):
    """
    Obtiene los datos de ingresos de estudiantes y docentes para una fecha específica.
    """
    conn = None
    try:
        conn = db_pool.get_conn()
        cur = conn.cursor()

        # Define el inicio y el fin del día seleccionado
        start_of_day = datetime.combine(selected_date, datetime.min.time())
        end_of_day = datetime.combine(selected_date, datetime.max.time())

        # Consulta para contar ingresos de estudiantes y docentes para la fecha específica
        cur.execute(
            """
            SELECT 'Estudiantes' AS tipo, COUNT(*) AS cantidad FROM ingresos_estudiantes 
            WHERE hora_ingreso BETWEEN %s AND %s
            UNION ALL
            SELECT 'Docentes' AS tipo, COUNT(*) AS cantidad FROM ingresos_docentes 
            WHERE hora_ingreso BETWEEN %s AND %s;
            """,
            (start_of_day, end_of_day, start_of_day, end_of_day)
        )
        data = cur.fetchall()
        
        df = pd.DataFrame(data, columns=['tipo', 'cantidad'])
        return df

    except Exception as e:
        st.error(f"Error al conectar o consultar la base de datos: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            db_pool.put_conn(conn)

def create_dashboard():
    """
    Crea el dashboard con Streamlit, incluyendo un selector de fecha única.
    """
    st.set_page_config(page_title="Dashboard de Asistencia", layout="wide")
    st.title('📊 Dashboard de Asistencia por Fecha')

    # Nuevo: Selector de fecha única para el usuario
    today = datetime.now().date()
    selected_date = st.date_input("Seleccione una Fecha", today)

    # Pasar la fecha seleccionada a la función de obtención de datos
    df = get_data_for_dashboard(selected_date)

    if not df.empty and df['cantidad'].sum() > 0:
        col1, col2 = st.columns(2)

        # Gráfico de barras verticales
        with col1:
            st.header(f'Ingresos de Estudiantes y Docentes ({selected_date.strftime("%d-%m-%Y")})')
            fig_bar = px.bar(
                df, 
                x='tipo', 
                y='cantidad', 
                title='Cantidad de Ingresos por Tipo de Persona',
                labels={'tipo': 'Tipo de Persona', 'cantidad': 'Cantidad de Ingresos'},
                color='tipo'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Gráfico de pastel (pie chart)
        with col2:
            st.header('Distribución de Ingresos')
            fig_pie = px.pie(
                df, 
                values='cantidad', 
                names='tipo',
                title='Proporción de Estudiantes vs. Docentes'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info(f"No hay registros de ingresos para la fecha seleccionada ({selected_date.strftime('%d-%m-%Y')}) o no se pudieron cargar los datos.")

if __name__ == '__main__':
    create_dashboard()