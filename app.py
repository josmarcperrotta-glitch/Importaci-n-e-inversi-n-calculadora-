import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Dashboard Financiero e Inversiones Pro", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard Financiero y Control de Activos Pro (RD)")
st.markdown("Control integral de cuentas, tarjetas de crédito, presupuestos, vehículos (DGA/DGII) e inversiones variadas.")

# Inicializar estados de datos (Session State)
if 'cuentas' not in st.session_state:
    st.session_state.cuentas = pd.DataFrame([
        {'Cuenta': 'Banco Nacional', 'Tipo': 'Cuenta Corriente', 'Saldo': 120600.0},
        {'Cuenta': 'Banco Money Pro', 'Tipo': 'Cuenta Corriente', 'Saldo': 148141.87},
        {'Cuenta': 'Cartera USD', 'Tipo': 'Efectivo', 'Saldo': 52200.0}, # Aprox con tasa
        {'Cuenta': 'Casa', 'Tipo': 'Activo Fijo', 'Saldo': 5452000.0},
        {'Cuenta': 'Moto', 'Tipo': 'Activo Fijo', 'Saldo': 200000.0}
    ])

if 'tarjetas' not in st.session_state:
    st.session_state.tarjetas = pd.DataFrame([
        {'Tarjeta': 'Banco Money Pro', 'Deuda / Balance': -5000.0},
        {'Tarjeta': 'Banco Nacional', 'Deuda / Balance': 7841.0}
    ])

if 'transacciones' not in st.session_state:
    st.session_state.transacciones = pd.DataFrame([
        {'Fecha': '2026-06-16', 'Tipo': 'Gasto', 'Categoría': 'Formación', 'Cuenta': 'Banco Money Pro', 'Descripción': 'Curso', 'Monto': 2500.0, 'ITBIS': 0.0},
        {'Fecha': '2026-06-16', 'Tipo': 'Gasto', 'Categoría': 'Cafe', 'Cuenta': 'Banco Money Pro', 'Descripción': 'Cafetería', 'Monto': 3000.0, 'ITBIS': 540.0},
        {'Fecha': '2026-06-20', 'Tipo': 'Ingreso', 'Categoría': 'Negocio', 'Cuenta': 'Banco Money Pro', 'Descripción': 'Ventas', 'Monto': 20000.0, 'ITBIS': 0.0},
        {'Fecha': '2026-06-01', 'Tipo': 'Ingreso', 'Categoría': 'Salario', 'Cuenta': 'Banco Money Pro', 'Descripción': 'Nomina', 'Monto': 45000.0, 'ITBIS': 0.0}
    ])

if 'presupuestos' not in st.session_state:
    st.session_state.presupuestos = pd.DataFrame([
        {'Categoría': 'Ropa', 'Límite': 7000.0},
        {'Categoría': 'Casa', 'Límite': 6500.0},
        {'Categoría': 'Cafe', 'Límite': 4500.0},
        {'Categoría': 'Formación', 'Límite': 5000.0},
        {'Categoría': 'Vehículo', 'Límite': 1000.0},
        {'Categoría': 'Servicios', 'Límite': 800.0}
    ])

if 'vehiculos' not in st.session_state:
    st.session_state.vehiculos = pd.DataFrame(columns=[
        'Vehículo', 'FOB / Valor Compra', 'Flete y Seguro (CIF)', 'Arancel DGA (20%)', 
        'ITBIS DGII (18%)', 'Primera Placa / Emisión', 'Repuestos/Mantenimiento', 
        'Gastos Operativos', 'Valor Actual Estimado'
    ])

if 'inversiones' not in st.session_state:
    st.session_state.inversiones = pd.DataFrame(columns=['Activo', 'Tipo', 'Capital Invertido', 'Valor Actual'])

# Navegación lateral
menu = st.sidebar.selectbox("Navegación", [
    "Saldo y Cuentas", 
    "Ingresos, Gastos y Transacciones", 
    "Presupuestos y Límites", 
    "Inversión e Importación de Vehículos", 
    "Inversiones Variadas"
])

if menu == "Saldo y Cuentas":
    st.header("💳 Control de Cuentas, Tarjetas y Otros Activos")
    
    # Calcular saldos totales
    total_cuentas = st.session_state.cuentas['Saldo'].sum() if not st.session_state.cuentas.empty else 0.0
    total_tarjetas = st.session_state.tarjetas['Deuda / Balance'].sum() if not st.session_state.tarjetas.empty else 0.0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Saldo Cuentas Corrientes / Efectivo", f"${total_cuentas:,.2f}")
    col2.metric("Balance Tarjetas de Crédito", f"${total_tarjetas:,.2f}")
    col3.metric("Patrimonio Líquido Estimado", f"${(total_cuentas + total_tarjetas):,.2f}")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Cuentas y Efectivo")
        st.dataframe(st.session_state.cuentas, use_container_width=True)
        
        with st.form("form_nueva_cuenta"):
            st.write("Agregar Cuenta / Activo Fijo")
            nombre_cta = st.text_input("Nombre (Ej. Banco BHD, Casa, Cripto)")
            tipo_cta = st.selectbox("Tipo", ["Cuenta Corriente", "Ahorros", "Efectivo", "Activo Fijo"])
            saldo_cta = st.number_input("Saldo / Valor Inicial ($)", min_value=0.0, step=100.0)
            if st.form_submit_button("Añadir Cuenta"):
                nova = pd.DataFrame([{'Cuenta': nombre_cta, 'Tipo': tipo_cta, 'Saldo': saldo_cta}])
                st.session_state.cuentas = pd.concat([st.session_state.cuentas, nova], ignore_index=True)
                st.success("Cuenta agregada con éxito.")
                st.rerun()

    with c2:
        st.subheader("Tarjetas de Crédito")
        st.dataframe(st.session_state.tarjetas, use_container_width=True)
        
        with st.form("form_nueva_tarjeta"):
            st.write("Agregar Tarjeta de Crédito")
            nombre_tc = st.text_input("Nombre de Tarjeta")
            deuda_tc = st.number_input("Balance / Deuda actual ($)", step=50.0)
            if st.form_submit_button("Añadir Tarjeta"):
                nova_tc = pd.DataFrame([{'Tarjeta': nombre_tc, 'Deuda / Balance': deuda_tc}])
                st.session_state.tarjetas = pd.concat([st.session_state.tarjetas, nova_tc], ignore_index=True)
                st.success("Tarjeta agregada con éxito.")
                st.rerun()

elif menu == "Ingresos, Gastos y Transacciones":
    st.header("📝 Registro y Historial de Transacciones")
    
    with st.form("form_transaccion"):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha", datetime.now())
            tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
            monto = st.number_input("Monto Total ($)", min_value=0.0, step=10.0)
        with col2:
            categoria = st.selectbox("Categoría", ["Salario", "Negocio", "Ropa", "Casa", "Cafe", "Formación", "Vehículo", "Servicios", "Otros"])
            cuenta_asoc = st.selectbox("Cuenta Asociada", st.session_state.cuentas['Cuenta'].tolist() if not st.session_state.cuentas.empty else ["General"])
            incluye_itbis = st.checkbox("¿Calcula ITBIS (18%)?")
            
        descripcion = st.text_input("Descripción / Notas")
        submitted = st.form_submit_button("Registrar Transacción")
        
        if submitted:
            val_itbis = round(monto * 0.18, 2) if incluye_itbis else 0.0
            nueva_fila = pd.DataFrame({
                'Fecha': [str(fecha)], 'Tipo': [tipo], 'Categoría': [categoria], 
                'Cuenta': [cuenta_asoc], 'Descripción': [descripcion], 'Monto': [monto], 'ITBIS': [val_itbis]
            })
            st.session_state.transacciones = pd.concat([st.session_state.transacciones, nueva_fila], ignore_index=True)
            st.success("¡Transacción registrada con éxito!")
            st.rerun()

    st.subheader("Listado General de Transacciones")
    df_t = st.session_state.transacciones
    st.dataframe(df_t, use_container_width=True)
    
    if not df_t.empty and not df_t[df_t['Tipo'] == 'Gasto'].empty:
        st.divider()
        st.subheader("Gráfico de Distribución de Gastos (Donut)")
        df_gastos = df_t[df_t['Tipo'] == 'Gasto']
        fig_donut = px.pie(df_gastos, values='Monto', names='Categoría', hole=0.5, title="Gastos por Categoría")
        st.plotly_chart(fig_donut, use_container_width=True)

elif menu == "Presupuestos y Límites":
    st.header("🎯 Control de Presupuestos y Límites por Categoría")
    st.markdown("Compara tus gastos reales frente a los límites presupuestados tal como en la app de referencia.")
    
    df_t = st.session_state.transacciones
    df_p = st.session_state.presupuestos
    
    if not df_t.empty and not df_p.empty:
        gastos_por_cat = df_t[df_t['Tipo'] == 'Gasto'].groupby('Categoría')['Monto'].sum().reset_index()
        df_merged = pd.merge(df_p, gastos_por_cat, on='Categoría', how='left').fillna(0)
        df_merged.rename(columns={'Monto': 'Gastado'}, inplace=True)
        df_merged['Disponible'] = df_merged['Límite'] - df_merged['Gastado']
        
        st.dataframe(df_merged, use_container_width=True)
        
        # Gráfico de barras comparativo Gastado vs Límite
        fig_presupuesto = go.Figure(data=[
            go.Bar(name='Gastado', x=df_merged['Categoría'], y=df_merged['Gastado'], marker_color='orange'),
            go.Bar(name='Límite Presupuesto', x=df_merged['Categoría'], y=df_merged['Límite'], marker_color='lightblue')
        ])
        fig_presupuesto.update_layout(barmode='group', title="Gastos Reales vs Límites Presupuestarios")
        st.plotly_chart(fig_presupuesto, use_container_width=True)
    else:
        st.info("Faltan datos de transacciones o presupuestos para mostrar la comparativa.")

elif menu == "Inversión e Importación de Vehículos":
    st.header("🚗 Importación, Impuestos Aduanales (DGA) e ITBIS (DGII)")
    
    with st.form("form_vehiculo"):
        vehiculo = st.text_input("Modelo / Descripción del Vehículo (Ej. Audi A4 B8.5 o Kia Forte)")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            fob = st.number_input("Valor FOB Compra ($)", min_value=0.0, step=100.0)
            flete_seguro = st.number_input("Flete y Seguro ($)", min_value=0.0, step=50.0)
        with c2:
            arancel_pct = st.slider("Arancel DGA (%)", min_value=0.0, max_value=30.0, value=20.0, step=1.0)
            primera_placa = st.number_input("Gastos Primera Placa / Emisión ($)", min_value=0.0, step=50.0)
        with c3:
            repuestos = st.number_input("Repuestos, Talleres y Reparaciones ($)", min_value=0.0, step=50.0)
            gastos_op = st.number_input("Otros Gastos Operativos ($)", min_value=0.0, step=50.0)
            
        valor_actual = st.number_input("Valor de Mercado Actual Estimado ($)", min_value=0.0, step=100.0)
            
        submitted_v = st.form_submit_button("Calcular y Guardar Vehículo")
        
        if submitted_v and vehiculo:
            cif = fob + flete_seguro
            val_arancel = round(cif * (arancel_pct / 100.0), 2)
            val_itbis_dgii = round((cif + val_arancel) * 0.18, 2)
            
            nueva_v = pd.DataFrame({
                'Vehículo': [vehiculo], 'FOB / Valor Compra': [fob], 
                'Flete y Seguro (CIF)': [flete_seguro], 'Arancel DGA (20%)': [val_arancel],
                'ITBIS DGII (18%)': [val_itbis_dgii], 'Primera Placa / Emisión': [primera_placa], 
                'Repuestos/Mantenimiento': [repuestos], 'Gastos Operativos': [gastos_op], 
                'Valor Actual Estimado': [valor_actual]
            })
            st.session_state.vehiculos = pd.concat([st.session_state.vehiculos[st.session_state.vehiculos['Vehículo'] != vehiculo], nueva_v], ignore_index=True)
            st.success(f"Vehículo '{vehiculo}' guardado correctamente.")
            st.rerun()

    if not st.session_state.vehiculos.empty:
        st.subheader("Portafolio y Desglose Fiscal de Vehículos")
        df_v_display = st.session_state.vehiculos.copy()
        df_v_display['Costo Total Invertido'] = (
            df_v_display['FOB / Valor Compra'] + df_v_display['Flete y Seguro (CIF)'] + 
            df_v_display['Arancel DGA (20%)'] + df_v_display['ITBIS DGII (18%)'] + 
            df_v_display['Primera Placa / Emisión'] + df_v_display['Repuestos/Mantenimiento'] + 
            df_v_display['Gastos Operativos']
        )
        df_v_display['Ganancia / Pérdida Potencial'] = df_v_display['Valor Actual Estimado'] - df_v_display['Costo Total Invertido']
        st.dataframe(df_v_display, use_container_width=True)

elif menu == "Inversiones Variadas":
    st.header("📈 Inversiones Variadas (Criptomonedas, Proyectos, etc.)")
    
    with st.form("form_inversion"):
        activo = st.text_input("Nombre del Activo (Ej. Bitcoin / P2P Binance)")
        tipo_inv = st.selectbox("Tipo de Activo", ["Criptomonedas", "Acciones / Fondos", "Bienes Raíces", "Préstamos / Otros"])
        c1, c2 = st.columns(2)
        with c1:
            capital = st.number_input("Capital Inicial Invertido ($)", min_value=0.0, step=50.0)
        with c2:
            valor_act = st.number_input("Valor Actual de Mercado ($)", min_value=0.0, step=50.0)
            
        submitted_i = st.form_submit_button("Registrar Inversión")
        
        if submitted_i and activo:
            nueva_inv = pd.DataFrame({'Activo': [activo], 'Tipo': [tipo_inv], 'Capital Invertido': [capital], 'Valor Actual': [valor_act]})
            st.session_state.inversiones = pd.concat([st.session_state.inversiones[st.session_state.inversiones['Activo'] != activo], nueva_inv], ignore_index=True)
            st.success(f"Inversión en '{activo}' registrada.")
            st.rerun()

    if not st.session_state.inversiones.empty:
        st.subheader("Resumen de Inversiones Variadas")
        df_i_display = st.session_state.inversiones.copy()
        df_i_display['Ganancia / Pérdida ($)'] = df_i_display['Valor Actual'] - df_i_display['Capital Invertido']
        df_i_display['Rentabilidad (%)'] = ((df_i_display['Ganancia / Pérdida ($)'] / df_i_display['Capital Invertido']) * 100).round(2)
        st.dataframe(df_i_display, use_container_width=True)
