import streamlit as st

# Initialize session state for tax rates and parameters
if 'tax_rates' not in st.session_state:
    st.session_state.tax_rates = {
        'simples_nacional_rate': 0.09,
        'pro_labore_rate': 0.28,
        'inss_pro_labore_rate': 0.11,
        'contador_value': 300.0,
        'vale_transporte_rate': 0.06
    }

@st.cache_data
def calculate_inss(gross_salary):
    inss = 0
    if gross_salary <= 1412:
        inss = gross_salary * 0.075
        aliquota = "7,5%"
    elif gross_salary <= 2666.68:
        inss = (1412 * 0.075) + ((gross_salary - 1412) * 0.09)
        aliquota = "9%"
    elif gross_salary <= 4000.03:
        inss = (1412 * 0.075) + ((2666.68 - 1412) * 0.09) + ((gross_salary - 2666.68) * 0.12)
        aliquota = "12%"
    elif gross_salary <= 7786.02:
        inss = (1412 * 0.075) + ((2666.68 - 1412) * 0.09) + ((4000.03 - 2666.68) * 0.12) + ((gross_salary - 4000.03) * 0.14)
        aliquota = "14%"
    else:
        inss = (1412 * 0.075) + ((2666.68 - 1412) * 0.09) + ((4000.03 - 2666.68) * 0.12) + ((7786.02 - 4000.03) * 0.14)
        aliquota = "Teto"
    
    aliquota_efetiva = (inss / gross_salary) * 100
    return inss, aliquota, aliquota_efetiva

@st.cache_data
def calculate_irrf(base):
    if base <= 2259.20:
        return 0, "Isento", 0
    elif base <= 2826.65:
        irrf = (base * 0.075) - 169.44
        aliquota = "7,5%"
    elif base <= 3751.05:
        irrf = (base * 0.15) - 381.44
        aliquota = "15%"
    elif base <= 4664.68:
        irrf = (base * 0.225) - 662.77
        aliquota = "22,5%"
    else:
        irrf = (base * 0.275) - 896.00
        aliquota = "27,5%"
    
    aliquota_efetiva = (irrf / base) * 100 if base > 0 else 0
    return irrf, aliquota, aliquota_efetiva

@st.dialog("Gerenciar Parâmetros")
def show_parameter_dialog():
    st.write("### Parâmetros PJ")
    st.session_state.tax_rates['simples_nacional_rate'] = st.number_input(
        "Taxa Simples Nacional (%)", 
        value=st.session_state.tax_rates['simples_nacional_rate']*100,
        step=0.1
    ) / 100
    st.session_state.tax_rates['pro_labore_rate'] = st.number_input(
        "Percentual Pró-Labore (%)", 
        value=st.session_state.tax_rates['pro_labore_rate']*100,
        step=0.1
    ) / 100
    st.session_state.tax_rates['inss_pro_labore_rate'] = st.number_input(
        "Taxa INSS sobre Pró-Labore (%)", 
        value=st.session_state.tax_rates['inss_pro_labore_rate']*100,
        step=0.1
    ) / 100
    st.session_state.tax_rates['contador_value'] = st.number_input(
        "Valor Contador (R$)", 
        value=st.session_state.tax_rates['contador_value'],
        step=10.0
    )
    
    st.write("### Parâmetros CLT")
    st.session_state.tax_rates['vale_transporte_rate'] = st.number_input(
        "Taxa Vale Transporte (%)", 
        value=st.session_state.tax_rates['vale_transporte_rate']*100,
        step=0.1
    ) / 100
    
    if st.button("Salvar"):
        st.rerun()

def calculate_pj_taxes(gross_value):
    rates = st.session_state.tax_rates
    simples_nacional = gross_value * rates['simples_nacional_rate']
    pro_labore = gross_value * rates['pro_labore_rate']
    inss_pro_labore = pro_labore * rates['inss_pro_labore_rate']
    contador = rates['contador_value']
    
    irrf_base = pro_labore - inss_pro_labore
    irrf, irrf_aliquota, irrf_efetiva = calculate_irrf(irrf_base)
    
    return {
        f"Simples Nacional ({rates['simples_nacional_rate']*100:.1f}%)": simples_nacional,
        f"INSS sobre Pró-Labore ({rates['inss_pro_labore_rate']*100:.1f}% de {rates['pro_labore_rate']*100:.1f}%)": inss_pro_labore,
        f"IRRF sobre Pró-Labore (Alíquota: {irrf_aliquota} | Efetiva: {irrf_efetiva:.1f}%)": irrf,
        "Contador": contador
    }

st.set_page_config(layout="wide")
st.title("Simulador CLT x PJ")

# Input row with salary and parameters button
col_input, col_params = st.columns([6, 1], vertical_alignment="bottom")
with col_input:
    gross_value = st.number_input("Digite o valor bruto recebido (R$):", min_value=0.0, value=5000.0, step=100.0)
with col_params:
    if st.button("⚙️ Parâmetros", use_container_width=True):
        show_parameter_dialog()

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cenário CLT")
    
    # CLT Calculations
    inss, inss_aliquota, inss_efetiva = calculate_inss(gross_value)
    irrf_base = gross_value - inss
    irrf, irrf_aliquota, irrf_efetiva = calculate_irrf(irrf_base)
    vale_transporte = gross_value * st.session_state.tax_rates['vale_transporte_rate']
    
    clt_deductions = {
        f"INSS (Alíquota: {inss_aliquota} | Efetiva: {inss_efetiva:.1f}%)": inss,
        f"IRRF (Alíquota: {irrf_aliquota} | Efetiva: {irrf_efetiva:.1f}%)": irrf,
        f"Vale Transporte ({st.session_state.tax_rates['vale_transporte_rate']*100:.1f}%)": vale_transporte,
    }
    
    total_clt_deductions = sum(clt_deductions.values())
    liquid_clt = gross_value - total_clt_deductions
    
    with st.container(border=True):
        st.write("### Descontos:")
        for item, value in clt_deductions.items():
            st.write(f"{item}: R$ {value:.2f}")
    
    with st.container(border=True):
        st.write("### Resumo:")
        st.write(f"Total de descontos: R$ {total_clt_deductions:.2f}")
        st.write(f"**Valor Líquido: R$ {liquid_clt:.2f}**")
        st.write(f"Percentual líquido: {(liquid_clt/gross_value)*100:.1f}%")

with col2:
    st.subheader("Cenário PJ")
    
    # PJ Calculations
    pj_deductions = calculate_pj_taxes(gross_value)
    total_pj_deductions = sum(pj_deductions.values())
    liquid_pj = gross_value - total_pj_deductions
    
    with st.container(border=True):
        st.write("### Descontos:")
        for item, value in pj_deductions.items():
            st.write(f"{item}: R$ {value:.2f}")
    
    with st.container(border=True):
        st.write("### Resumo:")
        st.write(f"Total de descontos: R$ {total_pj_deductions:.2f}")
        st.write(f"**Valor Líquido: R$ {liquid_pj:.2f}**")
        st.write(f"Percentual líquido: {(liquid_pj/gross_value)*100:.1f}%")

st.write("---")
with st.container(border=True):
    st.write("### Comparativo Final")
    difference = liquid_pj - liquid_clt
    percentage_difference = (difference / liquid_clt) * 100

    col3, col4 = st.columns(2)
    with col3:
        st.write(f"Diferença absoluta (PJ - CLT): R$ {difference:.2f}")
    with col4:
        st.write(f"Diferença percentual: {percentage_difference:.1f}%")

st.info("""
**Observações importantes:**
- Os cálculos são aproximados e podem variar conforme situações específicas
- Para PJ, considere reservas para férias, 13º e benefícios
- Consulte um contador para análises mais precisas
- Os valores não incluem benefícios como plano de saúde, VA/VR, etc.
""") 