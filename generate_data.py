import pandas as pd
import numpy as np

def calculate_inss(gross_salary):
    inss = 0
    if gross_salary <= 1412:
        inss = gross_salary * 0.075
    elif gross_salary <= 2666.68:
        inss = (1412 * 0.075) + ((gross_salary - 1412) * 0.09)
    elif gross_salary <= 4000.03:
        inss = (1412 * 0.075) + ((2666.68 - 1412) * 0.09) + ((gross_salary - 2666.68) * 0.12)
    elif gross_salary <= 7786.02:
        inss = (1412 * 0.075) + ((2666.68 - 1412) * 0.09) + ((4000.03 - 2666.68) * 0.12) + ((gross_salary - 4000.03) * 0.14)
    else:
        inss = (1412 * 0.075) + ((2666.68 - 1412) * 0.09) + ((4000.03 - 2666.68) * 0.12) + ((7786.02 - 4000.03) * 0.14)
    return inss

def calculate_irrf(base):
    if base <= 2259.20:
        return 0
    elif base <= 2826.65:
        return (base * 0.075) - 169.44
    elif base <= 3751.05:
        return (base * 0.15) - 381.44
    elif base <= 4664.68:
        return (base * 0.225) - 662.77
    else:
        return (base * 0.275) - 896.00

def calculate_clt_liquid(gross):
    inss = calculate_inss(gross)
    irrf = calculate_irrf(gross - inss)
    vale_transporte = gross * 0.06
    return gross - inss - irrf - vale_transporte

def calculate_pj_liquid(gross):
    simples_nacional = gross * 0.09
    pro_labore = gross * 0.28
    inss_pro_labore = pro_labore * 0.11
    contador = 300.0
    
    irrf_base = pro_labore - inss_pro_labore
    irrf = calculate_irrf(irrf_base)
    
    return gross - simples_nacional - inss_pro_labore - irrf - contador

def generate_comparison_data():
    # Gerar valores brutos de 1000 a 100000, incrementando de 100 em 100
    gross_values = np.arange(1000, 100100, 100)
    
    # Calcular valores líquidos
    clt_values = [calculate_clt_liquid(x) for x in gross_values]
    pj_values = [calculate_pj_liquid(x) for x in gross_values]
    
    # Criar DataFrame
    df = pd.DataFrame({
        'bruto': gross_values,
        'clt': clt_values,
        'pj': pj_values
    })
    
    # Salvar CSV
    df.to_csv('salary_comparison.csv', index=False)
    print("Arquivo salary_comparison.csv gerado com sucesso!")

if __name__ == "__main__":
    generate_comparison_data() 