import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
import unicodedata
import pages.home as home  # asumiendo que el código anterior está en pages/home.py

def crear_pagina_prediccion():
    st.title("Predicción de Causa de Muerte")
    st.write("Por favor, complete el siguiente formulario para obtener una predicción.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            sexo = st.selectbox(
                "Sexo",
                options=['Hombre', 'Mujer']
            )
            
            edad = st.number_input(
                "Edad",
                min_value=0,
                max_value=120,
                value=30
            )
            
            ocupacion = st.selectbox(
                "Ocupación",
                options=['Profesores y especialistas en docencia', 'No trabaja',
       'Trabajadores en la preparación y servicio de alimentos y bebidas, así como en servicios de esparcimiento y de hotelería',
       'Trabajadores en actividades agrícolas y ganaderas',
       'Ocupaciones insuficientemente especificadas',
       'Conductores de transporte y de maquinaria móvil',
       'Auxiliares y técnicos en ciencias exactas, biológicas, ingeniería, informática y en telecomunicaciones',
       'Otros trabajadores en actividades elementales y de apoyo, no clasificados anteriormente',
       'No aplica a menores de 5 años',
       'Trabajadores en la extracción y la edificación de construcciones',
       'Otros trabajadores artesanales no clasificados anteriormente',
       'Comerciantes en establecimientos', 'No especificada',
       'Empleados de ventas en establecimientos',
       'Otros operadores de maquinaria industrial, ensambladores y conductores de transporte, no clasificados anteriormente',
       'Artesanos y trabajadores en la elaboración de productos de madera, papel, textiles y de cuero y piel',
       'Médicos, enfermeras y otros especialistas en salud',
       'Investigadores y profesionistas en ciencias exactas, biológicas, ingeniería, informática y en telecomunicaciones',
       'Profesionistas en ciencias económico-administrativas, ciencias sociales, humanistas y en artes',
       'Trabajadores en la elaboración y procesamiento de alimentos, bebidas y productos de tabaco',
       'Otros trabajadores auxiliares en actividades administrativas, no clasificados anteriormente',
       'Auxiliares y técnicos en ciencias económico-administrativas, ciencias sociales, humanistas y en artes',
       'Supervisores de personal de apoyo administrativo, secretarias, capturistas, cajeros y trabajadores de control de archivo y transporte',
       'Artesanos y trabajadores en el tratamiento y elaboración de productos de metal',
       'Trabajadores en servicios de protección y vigilancia',
       'Auxiliares y técnicos en educación, instructores y capacitadores',
       'Trabajadores en cuidados personales y del hogar',
       'Enfermeras, técnicos en medicina y trabajadores de apoyo en salud',
       'Trabajadores domésticos, de limpieza, planchadores y otros trabajadores de limpieza',
       'Artesanos y trabajadores en la elaboración de productos de cerámica, vidrio, azulejo y similares',
       'Otros profesionistas y técnicos no clasificados anteriormente',
       'Otros directores, funcionarios, gerentes, coordinadores y jefes de área, no clasificados anteriormente',
       'Ayudantes en la preparación de alimentos',
       'Directores y gerentes en servicios financieros, legales, administrativos y sociales',
       'Otros comerciantes, empleados en ventas y agentes de ventas en establecimientos, no clasificados anteriormente',
       'Ayudantes de conductores de transporte, conductores de transporte de tracción humana y animal y cargadores',
       'Trabajadores de la Armada, Ejército y Fuerza Aérea',
       'Trabajadores de paquetería, de apoyo para espectáculos, mensajeros y repartidores de mercancías',
       'Coordinadores y jefes de área en producción y tecnología',
       'Trabajadores de apoyo en la minería, construcción e industria',
       'Operadores de maquinaria agropecuaria y forestal',
       'Directores y gerentes en producción, tecnología y transporte',
       'Operadores de instalaciones y maquinaria industrial',
       'Artesanos y trabajadores en la elaboración de productos de hule, caucho, plásticos y de sustancias químicas',
       'Directores y gerentes de ventas, restaurantes, hoteles y otros establecimientos',
       'Funcionarios y altas autoridades de los sectores público, privado y social',
       'Coordinadores y jefes de área en servicios financieros, administrativos y sociales',
       'Supervisores y trabajadores que brindan y manejan información',
       'Trabajadores en actividades pesqueras, forestales, caza y similares',
       'Otros trabajadores en actividades agrícolas, ganaderas, forestales, caza y pesca, no clasificados anteriormente',
       'Vendedores ambulantes',
       'Trabajadores de apoyo en actividades agropecuarias, forestales, pesca y caza',
       'Coordinadores y jefes de área de ventas, restaurantes, hoteles y otros establecimientos',
       'Busca trabajo',
       'Ensambladores y montadores de herramientas, maquinaria, productos metálicos y electrónicos',
       'Trabajadores en servicios de alquiler']
            )
            
            edo_civil = st.selectbox(
                "Estado Civil",
                options=['Divorciado(a)', 'Soltero(a)', 'Viudo(a)', 'Casado(a)',
       'Unión libre', 'No aplica a menores de 12 años', 'No especificado',
       'Separado(a)']
            )
            
            cond_act = st.selectbox(
                "Condición de Actividad",
                options=['Sí', 'No', 'No aplica a menores de 5 años', 'Se ignora']
            )
            
            derechohab = st.selectbox(
                "Derechohabiencia",
                options=['IMSS', 'Ninguna', 'No especificada', 'Otra', 'ISSSTE', 'IMSS BIENESTAR', 'SEDENA', 'ISSFAM', 'PEMEX', 'SEMAR']
            )

        with col2:
            ent_ocurr = st.selectbox(
                "Entidad de Ocurrencia",
                options=['Aguascalientes', 'Entidad no especificada', 'Jalisco',
       'Baja California', 'México', 'Baja California Sur', 'Campeche',
       'Yucatán', 'Tabasco', 'Coahuila de Zaragoza', 'Durango',
       'Nuevo León', 'Chihuahua', 'Tamaulipas', 'Hidalgo', 'Colima',
       'Chiapas', 'Oaxaca', 'Sonora', 'Sinaloa', 'Ciudad de México',
       'Veracruz de Ignacio de la Llave', 'Puebla', 'Guerrero', 'Nayarit',
       'Zacatecas', 'Guanajuato', 'Michoacán de Ocampo', 'Morelos',
       'San Luis Potosí', 'Tlaxcala', 'Querétaro', 'Quintana Roo']
            )
            
            tloc_resid = st.selectbox(
                "Tamaño de Localidad de Residencia",
                options=['5 000 a 9 999 habitantes', '500 000 a 999 999 habitantes',
       '1 a 999 habitantes', '1 000 a 1 999 habitantes',
       '15 000 a 19 999 habitantes', '10 000 a 14 999 habitantes',
       '20 000 a 29 999 habitantes', '30 000 a 39 999 habitantes',
       '2 500 a 4 999 habitantes', '50 000 a 74 999 habitantes',
       '2 000 a 2 499  habitantes', '250 000 a 499 999 habitantes',
       '40 000 a 49 999 habitantes', '100 000 a 249 999 habitantes',
       'No especificado', '1 500 000 y más habitantes',
       '1 000 000 a 1 499 999 habitantes', '75 000 a 99 999 habitantes']
            )
            
            mes_ocurr = st.selectbox(
                "Mes de Ocurrencia",
                options=list(range(1, 13))
            )
            
            horas = st.number_input(
                "Horas de la muerte",
                min_value=0,
                max_value=23,
                value=12
            )
            
            peso = st.number_input(
                "Peso (kg)",
                min_value=0,
                max_value=80,
                value=70
            )
            
            covid_influenza = st.selectbox(
                "¿Tuvo COVID o Influenza?",
                options=['Si', 'No']
            )

        submitted = st.form_submit_button("Obtener Predicción")

        if submitted:
            # Crear un DataFrame con los datos ingresados
            datos = pd.DataFrame({
                'sexo': [sexo],
                'edad_final': [edad],
                'ocupacion': [ocupacion],
                'edo_civil': [edo_civil],
                'cond_act': [cond_act],
                'derechohab': [derechohab],
                'ent_ocurr': [ent_ocurr],
                'tloc_resid': [tloc_resid],
                'mes_ocurr': [mes_ocurr],
                'horas': [horas],
                'Peso': [peso],
                'COVID_Influenza': [covid_influenza]
            })
            
            # Cargar el modelo
            try:
                model = load('/Users/lorenzoreinoso/Documents/defunciones_23_ML_P2/modelo_entrenado.joblib')
                
                # Quitar acentos de los datos
                datos = datos.applymap(lambda x: unicodedata.normalize('NFKD', str(x))
                                    .encode('ASCII', 'ignore')
                                    .decode('ASCII'))
                
                # Realizar la predicción
                prediccion = model.predict(datos)
                
                # Mostrar resultado
                st.success(f"Causa de muerte más probable: {prediccion[0]}")
                
                # Obtener probabilidades de predicción
                probabilidades = model.predict_proba(datos)
                clases = model.classes_
                
                # Mostrar las top 3 causas más probables
                top_3_idx = np.argsort(probabilidades[0])[-3:][::-1]
                st.write("Top 3 causas más probables:")
                for idx in top_3_idx:
                    st.write(f"- {clases[idx]}: {probabilidades[0][idx]*100:.2f}%")
                
            except Exception as e:
                st.error(f"Error al realizar la predicción: {str(e)}")

if __name__ == "__main__":
    crear_pagina_prediccion()