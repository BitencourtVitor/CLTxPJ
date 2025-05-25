# Simulador CLT x PJ 🧮

Este projeto é um simulador interativo desenvolvido em Streamlit que compara os custos e benefícios entre contratação CLT (Consolidação das Leis do Trabalho) e PJ (Pessoa Jurídica) no Brasil.

## 📋 Sobre o Projeto

O projeto nasceu de uma análise detalhada de dados e regulamentações tributárias brasileiras, coletados através de pesquisa e processamento com IA. Com base nesses dados, desenvolvi uma interface interativa que permite aos usuários:

- Comparar valores líquidos entre CLT e PJ
- Visualizar detalhadamente todos os descontos aplicáveis
- Ajustar parâmetros como taxas e valores de forma dinâmica
- Ver alíquotas efetivas de cada tributo

## 🧾 Cálculos Incluídos

### CLT
- INSS (com alíquotas progressivas)
- IRRF (com alíquotas e deduções)
- Vale Transporte (opcional)

### PJ
- Simples Nacional
- Pró-Labore
- INSS sobre Pró-Labore
- IRRF sobre Pró-Labore
- Custos com Contador

## 🚀 Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/CLTxPJ.git
cd CLTxPJ
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run app.py
```

## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Pandas

## 📊 Funcionalidades

- Interface limpa e intuitiva
- Cálculos em tempo real
- Visualização lado a lado para fácil comparação
- Parâmetros configuráveis via interface gráfica
- Cálculos de alíquotas efetivas
- Comparativo percentual entre modalidades

## ⚠️ Observações Importantes

- Os cálculos são aproximados e podem variar conforme situações específicas
- Para PJ, considere reservas para férias, 13º e benefícios
- Consulte um contador para análises mais precisas
- Os valores não incluem benefícios como plano de saúde, VA/VR, etc.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 