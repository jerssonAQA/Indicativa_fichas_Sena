import streamlit as st
import openai
import json
import pandas as pd
from tiktoken import encoding_for_model

# Configurar la API de OpenAI (usando secretos de Streamlit)
api_key = st.secrets.get("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key
else:
    st.error("No se encontró la clave OPENAI_API_KEY en st.secrets")
 


# Diccionario con file_ids y nombres de archivos en gpt-storage
file_dict = {'9538 - CENTRO DE COMERCIO Y TURISMO': 'file-KRHXtJo1wLmmbaAPmLQ9Cs',
 '9207 - CENTRO NACIONAL COLOMBO ALEMAN': 'file-DuWVX3GMFAAuPixdKeh2yR',
 '9304 - CENTRO DE COMERCIO Y SERVICIOS': 'file-6Ky7DUUiZPxa9e78Q4eKoS',
 '9204 - CENTRO DE TECNOLOGÍA DE LA MANUFACTURA AVANZADA.': 'file-QegU3RdyFFP91UWFFSu7YK',
 '9509 - CENTRO DE DESARROLLO AGROINDUSTRIAL Y EMPRESARIAL': 'file-NSfZfGytcnwURvVapnbPJy',
 '9105 - CENTRO INTERNACIONAL NÁUTICO, FLUVIAL Y PORTUARIO': 'file-148LSVpsK43AMXRi6B47X9',
 '9501 - COMPLEJO TECNOLOGICO PARA LA GESTION AGROEMPRESARIAL': 'file-1WFV1qreHRBi7u6oCGyqir',
 '9502 - COMPLEJO TECNOLÓGICO MINERO AGROEMPRESARIAL': 'file-KsJY1nYqK7eZspmie6wxMs',
 '9115 - CENTRO AGROPECUARIO Y DE BIOTECNOLOGIA EL PORVENIR': 'file-BqZz1NCDBc6tiH5CRegbGc',
 '9540 - CENTRO INDUSTRIAL Y DEL DESARROLLO TECNOLOGICO': 'file-FXFtytP2FU4bdZDwWP5sCo',
 '9525 - CENTRO AGROEMPRESARIAL Y DESARROLLO PECUARIO DEL HUILA': 'file-5Tp6aE6n7aDhD8gB8qoCTD',
 '9216 - CENTRO DE DISEÑO Y METROLOGIA': 'file-K1if3WMaq2r2axegB974D3',
 '9218 - CENTRO PARA LA INDUSTRIA PETROQUIMICA': 'file-RfrynoZSbeJkRpbU6xug8S',
 '9309 - CENTRO DE SERVICIOS EMPRESARIALES Y TURÍSTICOS': 'file-LdLXki5ZtUzGRY8iZRgVid',
 '9223 - CENTRO DE DISEÑO E INNOVACIÓN TECNOLÓGICA INDUSTRIAL': 'file-R3D2B54M4PRwZpj4U11u6R',
 '9503 - CENTRO DE LA INNOVACIÓN, LA AGROINDUSTRIA Y LA AVIACIÓN': 'file-T5rqTkzYxSbwEDvsDcEsi8',
 '9228 - CENTRO DE LA CONSTRUCCION': 'file-MMpNNouib81kLwEt5EzTes',
 '9522 - CENTRO DE RECURSOS NATURALES, INDUSTRIA Y BIODIVERSIDAD': 'file-STuZNYqVTVW6vbfcNG4fah',
 '9224 - CENTRO INDUSTRIAL DE MANTENIMIENTO INTEGRAL': 'file-SssG8V39FuyPcgAP52rCUE',
 '9404 - CENTRO DE GESTION ADMINISTRATIVA': 'file-NDWYDcdRgiceAi6cFXsrpp',
 '9205 - CENTRO TECNOLÓGICO DEL MOBILIARIO': 'file-XZNUmPwMuYFvmKbGeXG44r',
 '9103 - CENTRO PARA EL DESARROLLO AGROECOLÓGICO Y AGROINDUSTRIAL': 'file-PmqCsQZ67sFdVTUpQJ7CsD',
 '9126 - CENTRO NAUTICO PESQUERO DE BUENAVENTURA': 'file-Kdh11TXEYtkAFwUBFujHyu',
 '9511 - CENTRO DE LA TECNOLOGIA DEL DISEÑO Y LA PRODUCTIVIDAD EMPRESARIAL': 'file-XYmvoLHRvFSBbSpgygJdkB',
 '9303 - CENTRO DE GESTION DE MERCADOS, LOGISTICA Y TECNOLOGIAS DE LA INFORMACION': 'file-R4kx6sXyxZ38cByaJRFEj8',
 '9534 - CENTRO SUR COLOMBIANO DE LOGÍSTICA INTERNACIONAL': 'file-7qXQtwxXvmuothmBYHDsph',
 '9110 - CENTRO DE DESARROLLO AGROPECUARIO Y AGROINDUSTRIAL': 'file-52sCWbWyseHS7TD5y1LgVS',
 '9527 - CENTRO DE LA INDUSTRIA, LA EMPRESA Y LOS SERVICIOS': 'file-8cNmasSVe4j6Vky3JspnRj',
 '9104 - CENTRO AGROEMPRESARIAL Y MINERO': 'file-9GTMV2UFNRXb8xUjcFtnpR',
 '9543 - CENTRO DE TECNOLOGIAS AGROINDUSTRIALES': 'file-MGHHs67Zn2ZRVeFcFE5zgT',
 '9541 - CENTRO AGROTURÍSTICO': 'file-Fz6tJ1CkH9E95NNhKs2hfy',
 '9121 - CENTRO ATENCION SECTOR AGROPECUARIO': 'file-BQGHJdouT1JyUd6etCW8XF',
 '9536 - CENTRO INTERNACIONAL DE PRODUCCIÓN LIMPIA - LOPE': 'file-Kgh36HutRQDoon47nBGcL3',
 '9547 - CENTRO AMBIENTAL Y ECOTURISTICO DEL NORORIENTE AMAZONICO': 'file-BKJkJVxPBp86gQhqQotAaV',
 '9518 - CENTRO AGROFORESTAL Y ACUICOLA ARAPAIMA': 'file-XwaPy4Mqp3bnRJUvAABbkH',
 '9307 - CENTRO DE COMERCIO Y SERVICIOS': 'file-PHGQswLaKrW3Sbt6fuFiPG',
 '9515 - CENTRO PECUARIO Y AGROEMPRESARIAL': 'file-S6NBJhvWSBgH2n7L78ej2E',
 '9202 - CENTRO DE FORMACIÓN EN DISEÑO, CONFECCIÓN Y MODA.': 'file-Fi8PG7v615KQRh49uEox7L',
 '9122 - CENTRO ATENCION SECTOR AGROPECUARIO': 'file-3XYWktpRi1squHguw2nQYZ',
 '9504 - COMPLEJO TECNOLOGICO AGROINDUSTRIAL, PECUARIO Y TURISTICO': 'file-4uhWGE8727KJXiVb2wxMbT',
 '9530 - CENTRO DE GESTION Y DESARROLLO AGROINDUSTRIAL DE ARAUCA': 'file-ALB6QbfdoTX2qqM3skXwbU',
 '9213 - CENTRO DE TECNOLOGÍAS DEL TRANSPORTE': 'file-Gdjvb4uqGV3ymtmZikrZSU',
 '9405 - CENTRO DE SERVICIOS FINANCIEROS': 'file-WxyAGzMjMhahkhUu2vabPx',
 '9123 - CENTRO AGROPECUARIO LA GRANJA': 'file-A32acoyXi7bv94yK9DDfpH',
 '9119 - CENTRO DE FORMACIÓN PARA EL DESARROLLO RURAL Y MINERO': 'file-PnA8wVSiuTw3fEy7CgFAkZ',
 '9301 - CENTRO DE COMERCIO': 'file-Vxk4W9KhwBi7CMzQYxwDAB',
 '9535 - CENTRO AGROINDUSTRIAL Y PESQUERO DE LA COSTA PACIFICA': 'file-JMkJ4nvomMypNaqGK8AG8H',
 '9310 - CENTRO DE COMERCIO Y SERVICIOS': 'file-ScMdwe5fZsiU5QmXMduo4z',
 '9528 - CENTRO DE GESTION Y DESARROLLO SOSTENIBLE SURCOLOMBIANO': 'file-PKRoPBuMezypq7dQyNCnhW',
 '9510 - CENTRO AGROECOLOGICO Y EMPRESARIAL': 'file-TRvsBfhd86jQGXdUpjAaxa',
 '9203 - CENTRO PARA EL DESARROLLO DEL HABITAT Y LA CONSTRUCCIÓN': 'file-MVjwiDxEALP53Ffz4YCUd3',
 '9210 - CENTRO DE ELECTRICIDAD, ELECTRÓNICA Y TELECOMUNICACIONES': 'file-VAXnnJAizmvmXk3Q188bam',
 '9221 - CENTRO DE TELEINFORMÁTICA Y PRODUCCIÓN INDUSTRIAL': 'file-JjRjzMwpLCS6rLYR1rbPZB',
 '9537 - CENTRO DE LA INDUSTRIA, LA EMPRESA Y LOS SERVICIOS': 'file-BMYAwVJPy19JU5ySEeitKa',
 '9406 - CENTRO NACIONAL DE HOTELERIA, TURISMO Y ALIMENTOS': 'file-UG3h9uoiXakFAWTSsdf7mA',
 '9111 - CENTRO MINERO': 'file-T1uT2JocXUCdZyCs5ukbZG',
 '9514 - CENTRO INDUSTRIAL DE MANTENIMIENTO Y MANUFACTURA': 'file-2F98kZ5SRRu4nZrR31g3Fe',
 '9225 - CENTRO INDUSTRIAL DEL DISEÑO Y LA MANUFACTURA': 'file-Nb1Rbh15jSVNmz9GcEKWBu',
 '9231 - CENTRO PARA EL DESARROLLO TECNOLÓGICO DE LA CONSTRUCCIÓN Y LA INDUSTRIA': 'file-Ph2P4s1HrdgALoSnQndyEi',
 '9117 - CENTRO AGROINDUSTRIAL DEL META': 'file-CwEqjUqcu6cNWiLUpcMbHb',
 '9402 - CENTRO DE SERVICIOS Y GESTION EMPRESARIAL': 'file-DfTzDKrWRxrfQ3FQRKUhaL',
 '9206 - CENTRO TEXTIL Y DE GESTIÓN INDUSTRIAL': 'file-JNMx9zTK3x1otvph5GFSPn',
 '9517 - CENTRO PARA LA BIODIVERSIDAD Y EL TURISMO DEL AMAZONAS': 'file-8E6xEoEcoixgtPtyGVmT93',
 '9302 - CENTRO DE COMERCIO Y SERVICIOS': 'file-NPJRCsA9czmq7CmCMwK7K9',
 '9542 - CENTRO DE LA INNOVACION, LA TECNOLOGIA Y LOS SERVICIOS': 'file-Azv8JQW1KvKBkafWGKcdQc',
 '9529 - CENTRO DE LOGISTICA Y PROMOCION ECOTURISTICA DEL MAGDALENA': 'file-2E2ryaiWGCHFjxD8aKZ6iF',
 '9226 - CENTRO DE INDUSTRIA Y CONSTRUCCION': 'file-SEzN2v6TWgRUKWdzZzKcFX',
 '9209 - CENTRO DE TECNOLOGIAS PARA LA CONSTRUCCION Y LA MADERA': 'file-FoT1RSjFdBParp4NVYAHZH',
 '9232 - CENTRO INDUSTRIAL Y DE DESARROLLO EMPRESARIAL DE SOACHA': 'file-GordfuzUG2LodCne9SchMn',
 '9549 - COMPLEJO TECNOLOGICO, TURISTICO Y AGROINDUSTRIAL DEL OCCIDENTE ANTIOQUEÑO': 'file-X6eC3tnaLiGwAjPbxFuKsJ',
 '9513 - CENTRO DE DESARROLLO AGROEMPRESARIAL': 'file-FEXb7H6fS7r8yzvzBjrYQc',
 '9306 - CENTRO DE COMERCIO Y SERVICIOS': 'file-AHFuaT8JbuDzv6prHbyUc5',
 '9116 - CENTRO DE FORMACION AGROINDUSTRIAL': 'file-55gR7jjp1XW18gfJMj4FnP',
 '9212 - CENTRO DE MANUFACTURA EN TEXTILES Y CUERO': 'file-Gg3QQM832UsXv7faoqjZzG',
 '9222 - CENTRO INDUSTRIAL Y DE ENERGIAS ALTERNATIVAS': 'file-RXdWpNXKpRz1G7DUfXEsR6',
 '9127 - CENTRO DE FORMACIÓN MINERO AMBIENTAL': 'file-8segbDtkxR2pw73J1XW2qo',
 '9308 - CENTRO DE COMERCIO Y SERVICIOS': 'file-8H8uExHYdz3nd4WeRsGDQ8',
 '9545 - CENTRO AGROEMPRESARIAL Y TURISTICO DE LOS ANDES': 'file-2G9vz53AnTaZYztCVXtQ6C',
 '9229 - CENTRO DE DISEÑO TECNOLOGICO INDUSTRIAL': 'file-VRPWx6Y6LDBfZDqewWPfyK',
 '9311 - CENTRO DE GESTION TECNOLÓGICA DE SERVICIOS': 'file-1GfgNC9R7bHYLrhjnK7air',
 '9524 - CENTRO AGROEMPRESARIAL Y ACUICOLA': 'file-MQfFgJGgTB2YWDYpxpRFdU',
 '9227 - CENTRO DE ELECTRICIDAD Y AUTOMATIZACION INDUSTRIAL - CEAI': 'file-UfUps32EQ9iEQhYwnAxyMK',
 '9214 - CENTRO METALMECANICO': 'file-5FB3Rgy8P4W2qJGHQ5r8s3',
 '9220 - CENTRO DE PROCESOS INDUSTRIALES Y CONSTRUCCIÓN': 'file-Nj8ps2bSDi3Xp1AZqRYYsb',
 '9548 - CENTRO AGROPECUARIO Y DE SERVICIOS AMBIENTALES JIRI - JIRIMO': 'file-MpgAxjQDDErq36otvuPGdY',
 '9526 - CENTRO DE DESARROLLO AGROEMPRESARIAL Y TURISTICO DEL HUILA': 'file-H88mMFAg2pMSJv7aRnDYFp',
 '9217 - CENTRO PARA LA INDUSTRIA DE LA COMUNICACIÓN GRAFICA': 'file-Eht4XcMDThfeuSsbmtAHFb',
 '9403 - CENTRO DE FORMACION DE TALENTO HUMANO EN SALUD': 'file-82kciM9yfjAddMHvnQn7iQ',
 '9512 - CENTRO DE BIOTECNOLOGIA AGROPECUARIA': 'file-7sPDMWcYZdwJEL7r7hUHKJ',
 '9211 - CENTRO DE GESTION INDUSTRIAL': 'file-7yryQb5grZ5QrjzxBC4yVa',
 '9401 - CENTRO DE SERVICIOS DE SALUD': 'file-947iy16VgEESoEX4dU9uFj',
 '9531 - CENTRO DE PRODUCCIÓN Y TRANSFORMACION AGROINDUSTRIAL DE LA ORINOQUIA': 'file-ExhqpmByWsJAmhQ9tKhxNV',
 '9305 - CENTRO DE GESTION ADMINISTRATIVA Y FORTALECIMIENTO EMPRESARIAL': 'file-BfmQt6meiZTJYVjMVBMkdv',
 '9120 - CENTRO AGROINDUSTRIAL': 'file-RYEAAPrVxwGn1x4cRK5V95',
 '9201 - CENTRO DEL DISEÑO Y MANUFACTURA DEL CUERO': 'file-3cUvguEDzkzD6xP5fpGJL2',
 '9215 - CENTRO DE MATERIALES Y ENSAYOS': 'file-3CMA6N4KqeJKNgAB5aEBsc',
 '9523 - CENTRO DE COMERCIO, INDUSTRIA Y TURISMO DE CORDOBA': 'file-248HS5VjhumYdG2UbAAUbL',
 '9519 - CENTRO AGROINDUSTRIAL Y FORTALECIMIENTO EMPRESARIAL DE CASANARE': 'file-5pcZ8WSJ2Vz2f2d2eJLT4X',
 '9539 - CENTRO DE FORMACIÓN TURÍSTICA GENTE DE MAR Y DE SERVICIOS': 'file-9XQg5bGuyPXMCf3akgM4K8',
 '9516 - CENTRO TECNOLOGICO DE LA AMAZONIA': 'file-1QXWAbRW3dYDRZ7t8yeVWD',
 '9118 - CENTRO ACUICOLA Y AGROINDUSTRIAL DE GAIRA': 'file-SojWRr7RXzxgqYs1d7vxvA',
 '9125 - CENTRO LATINOAMERICANO DE ESPECIES MENORES': 'file-9VGJdZFtG677knHY3eA6ja',
 '9546 - CENTRO DE GESTION AGROEMPRESARIAL DEL ORIENTE': 'file-9SFeBDTx2ZWQm2q7CPnYFP',
 '9508 - CENTRO DE FORMACIÓN EN ACTIVIDAD FÍSICA Y CULTURA': 'file-JZkhMRi5gYXiuKayz3LCHb',
 '9532 - CENTRO DE INDUSTRIA Y SERVICIOS DEL META': 'file-4ZYpi2cT7QtFppwP8Cr99Z',
 '9533 - CENTRO DE DESARROLLO AGROINDUSTRIAL, TURISTICO Y TECNOLOGICO DEL GUAVIARE': 'file-9yrLBRX7A7T2qEZfS2JtS7',
 '9544 - CENTRO DE BIOTECNOLOGIA INDUSTRIAL': 'file-TLh9Y6r9mpDS15Fn3eNb3h',
 '9208 - CENTRO INDUSTRIAL Y DE AVIACION': 'file-CNig2BrbPB8Tz144FQXXUc',
 '9114 - CENTRO BIOTECNOLOGICO DEL CARIBE': 'file-2XN39b8r6BGcQT6XvxVEZD',
 '9113 - CENTRO AGROPECUARIO': 'file-Wc2HCEALUQYampancPvvD6',
 '9520 - CENTRO AGROEMPRESARIAL': 'file-BUHx7iwJyFGhnzWQjz6UC9',
 '9521 - CENTRO DE INNOVACIÓN Y DE GESTIÓN EMPRESARIAL Y CULTURAL': 'file-CSSGcW9v5aToVaY9YRH6Ks',
 '9112 - CENTRO PARA LA FORMACION CAFETERA': 'file-USFGHvscZwuYUHZgfeEFTT',
 '9101 - CENTRO DE LOS RECURSOS NATURALES RENOVABLES - LA SALADA': 'file-XGQ7FFbNJC14HW7fWbHV3g',
 '9124 - CENTRO AGROPECUARIO DE BUGA': 'file-KTuhTqvRNQHsHfpj6py2Fa',
 '9219 - CENTRO DE AUTOMATIZACION INDUSTRIAL': 'file-KNxyMPNKZDALp7ruxhdgKQ',
 '9230 - CENTRO NACIONAL DE ASISTENCIA TECNICA A LA INDUSTRIA - ASTIN': 'file-5bpvpm5YybWk62CecXAosV',
 '9551 - CENTRO DE LA INNOVACIÓN AGROINDUSTRIAL Y DE SERVICIOS': 'file-HM7Xg6vzea6t7C6eVSnrL3'}

# Funciones para cargar datos y realizar consultas a OpenAI
def load_file_content(file_id):
    """Obtiene el contenido del archivo de OpenAI GPT-Storage."""
    response = openai.File.download(file_id)
    file_content = response.decode("utf-8")
    lines = [json.loads(line) for line in file_content.split("\n") if line]
    return pd.DataFrame(lines)

def truncate_context_to_fit(context, max_tokens=7000):
    """Trunca el contexto para que no exceda el límite de tokens."""
    enc = encoding_for_model("gpt-4o-mini")
    tokens = enc.encode(context)
    if len(tokens) > max_tokens:
        truncated_tokens = tokens[:max_tokens]
        #raise ValueError("El contexto excede el límite permitido de tokens. Por favor, agrupa mejor los datos o selecciona menos columnas.")
        return enc.decode(truncated_tokens),1
    return context,0


def ask_openai(question, context):
    """Realiza una pregunta usando OpenAI GPT-4, pasando el contexto del archivo."""
    truncated_context,estado = truncate_context_to_fit(context)
    prompt = f"""
    Contexto: {truncated_context}
    Pregunta:{question}
            Proporciona números exactos y explica brevemente los resultados encontrados. 
            No generes código, solo describe los datos relevantes. 
            Si la pregunta no está relacionada con los datos, responde que no puedes contestarla.
    Respuesta:"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en interpretar datos de archivos."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"],estado

def columnas_agrupaciones(df,columnas):        
    funciones_agg={}    
    if columnas:
        columnas_numericas=['CUPO_APRENDICES','INSCRITOS','MATRICULADOS','EN_TRANSITO',
        'FORMACION','INDUCCION','CONDICIONADOS','APLAZADOS','RETIROS_VOLUNTARIOS',
        'CANC_VIRT_COMPLEMENTARIA','DESC_VIRT_COMPLEMENTARIA','CANCELADOS','REPROBADOS',
        'NO_APTOS','REINGRESADO','POR_CERTIFICAR','CERTIFICADOS','TRASLADADOS']
        # Identificar columnas numéricas no agrupadas
        
        columnas_a_agrupar = [
            col for col in df.columns if col in columnas_numericas #pd.api.types.is_numeric_dtype(df[col])
            ]
        columnas_no_agrupables=['CODIGO_CENTRO','NOMBRE_CENTRO','FECHA_INICIO','FECHA_FIN','PROGRAMA_FORMACION','VERSION_PROGRAMA','MUNICIPIO']
        # Verificar columnas específicas y contarlas si existen
        columnas_no_sumar = [col for col in df.columns if col not in columnas_a_agrupar and col not in columnas_no_agrupables and col not in columnas]
        columnas_contar_presentes=columnas_no_sumar
        # Crear diccionario para .agg 
        funciones_agg = {col: 'sum' for col in columnas_a_agrupar}
        for col in columnas_contar_presentes:
            funciones_agg[col] = 'nunique'
        columnas=[col for col in columnas if col not in columnas_a_agrupar]
        # Realizar la agrupación
        df_agrupado = df.groupby(columnas).agg(funciones_agg).reset_index()
        st.success("Datos agrupados con columnas numéricas sumadas:")
        return df_agrupado

# Interfaz de Streamlit
paso1=False
st.title("Aplicación Indicadores Fichas con IA")

# Selección del archivo
display_names = list(file_dict.keys())
selected_file = st.selectbox("Selecciona un archivo de GPT-Storage:", display_names)

if selected_file:
    file_id = file_dict[selected_file]
    st.info(f"Cargando contenido del archivo: {selected_file}")
    
    # Cargar y mostrar el contenido del archivo
    try:
        data = load_file_content(file_id)
        st.write("Vista previa de los datos:")
        st.dataframe(data)

        if 'FECHA_INICIO' in data.columns and 'FECHA_FIN' in data.columns:

            if data['FECHA_INICIO'].isnull().all() or data['FECHA_FIN'].isnull().all():
                st.error("Las columnas de fecha contienen valores no válidos o están vacías. Verifique los datos.")
            else:
                fecha_inicio = st.selectbox("Selecciona la fecha de inicio:",sorted(data['FECHA_INICIO'].unique()), index=0)
                # Ordenar las fechas de 'FECHA_FIN' de menor a mayor
                fechas_fin = sorted(data['FECHA_FIN'].unique())
                # Seleccionar el último valor como predeterminado
                fecha_fin = st.selectbox("Selecciona la fecha de fin:",fechas_fin,index=len(fechas_fin)-1)
                
                data = data[(data['FECHA_INICIO'] >= pd.to_numeric(fecha_inicio)) & (data['FECHA_FIN'] <= pd.to_numeric(fecha_fin))]

        if 'TIPO_PROGRAMA' in data.columns:
            tipo_programa = st.selectbox("Selecciona el tipo de programa:", ['TITULADA', 'COMPLEMENTARIA'])
            if tipo_programa:
                data = data[data['TIPO_PROGRAMA'] == tipo_programa]
                st.dataframe(data)
                paso1=True
            else:
                paso1=False

        columnas_disponibles = data.columns.tolist()
        columas_no_disponibles=['CODIGO_REGIONAL','NOMBRE_REGIONAL','CODIGO_CENTRO','DATOS_CENTRO','PROGRAMA_FORMACION','TIPO_PROGRAMA']
        columnas_disponibles=[col for col in columnas_disponibles if col not in  columas_no_disponibles]
        columnas_seleccionadas = st.multiselect("Selecciona obligatoriamente las columnas que deseas incluir en la consulta:", columnas_disponibles)
        # Mostrar columnas seleccionadas

        if columnas_seleccionadas:
            # Filtrar por rango de fechas
            agrupacion_columnas = columnas_agrupaciones(data, columnas_seleccionadas)
            agrupacion = agrupacion_columnas[columnas_seleccionadas]
            st.dataframe(agrupacion)
            paso2 = True
        else:
            st.info("Selecciona al menos una columna para mostrar.")
            paso2=False
        
        if paso2:
            # Convertir datos limitados a texto (para el contexto)
            context = agrupacion.to_string(index=False)

            # Caja de texto para la pregunta del usuario
            user_question = st.text_input("Haz una pregunta relacionada con los datos:")

            # Agregar botones para enviar la pregunta y limpiar el input
            col1, col2 = st.columns(2)
            enviar_pregunta = col1.button("Enviar Pregunta")
            limpiar_input = col2.button("Limpiar Pregunta")

            if limpiar_input:
                st.session_state["user_question"] = ""

            if enviar_pregunta and user_question:
                st.write("Generando respuesta...")
                response,estado = ask_openai(user_question, context)
                st.success("Respuesta:")
                if estado==0:
                    st.write(response)
                else:
                    st.write(response)  
                    raise ValueError("Si la respuesta no es la adecuada, se debe agrupar mejor los datos, ya que la cantidad de datos actuales excede el límite permitido.")

            
    except Exception as e:
        st.error(f"Error al cargar el archivo o procesar la solicitud: {e}")
