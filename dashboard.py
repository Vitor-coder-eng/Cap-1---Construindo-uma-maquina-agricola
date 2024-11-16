import streamlit as st
import cx_Oracle
import pandas as pd
import requests
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Função para conectar ao banco
def conectar_banco():
    dsn = 'oracle.fiap.com.br:1521/ORCL'
    return cx_Oracle.connect('rm559730', '240901', dsn)

# Função para obter dados
def obter_dados():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LEITURA_SENSORES")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Função para inserir dados
def inserir_dados(umidade, ph, nutriente_p, nutriente_k, irrigacao):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO LEITURA_SENSORES (UMIDADE, PH, NUTRIENTE_P, NUTRIENTE_K, IRRIGACAO) VALUES (:1, :2, :3, :4, :5)",
        (umidade, ph, nutriente_p, nutriente_k, irrigacao)
    )
    conn.commit()
    conn.close()

# Função para deletar dados
def deletar_dado(id_dado):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM LEITURA_SENSORES WHERE ID = :1", (id_dado,))
    conn.commit()
    conn.close()

# Função para obter previsão do tempo
def obter_previsao_tempo(cidade):
    try:
        api_key = "37916a05a8a64675b4a131649241611"
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={cidade}&lang=pt"
        response = requests.get(url)
        
        if response.status_code == 200:
            dados = response.json()
            previsao = {
                "Temperatura": f"{dados['current']['temp_c']}°C",
                "Sensação Térmica": f"{dados['current']['feelslike_c']}°C",
                "Condição": dados['current']['condition']['text'],
                "Umidade": f"{dados['current']['humidity']}%"
            }
            return previsao
        else:
            return {"Erro": "Não foi possível obter a previsão do tempo."}
    except Exception as e:
        return {"Erro": f"Erro ao obter previsão: {e}"}

# Função de previsão do modelo de irrigação
def previsao_irrigaçao(modelo, scaler, umidade, ph, nutriente_p, nutriente_k):
    dados_usuario = np.array([[umidade, ph, nutriente_p, nutriente_k]])
    dados_usuario_scaled = scaler.transform(dados_usuario)
    previsao = modelo.predict(dados_usuario_scaled)
    
    if previsao == 1:
        return "A bomba está LIGADA."
    else:
        return "A bomba está DESLIGADA."

# Treinando o modelo de previsão (exemplo simples)
dados_treinamento = {
    'Umidade': [60, 65, 70, 75, 80],
    'Ph': [6.5, 6.7, 6.8, 7.0, 7.2],
    'Nutriente_P': [0.5, 0.7, 0.8, 0.6, 0.9],
    'Nutriente_K': [0.6, 0.8, 0.7, 0.6, 0.9],
    'Irrigacao': [1, 1, 0, 1, 0]  # 1 = Ligada, 0 = Desligada
}

df_treinamento = pd.DataFrame(dados_treinamento)
X = df_treinamento[['Umidade', 'Ph', 'Nutriente_P', 'Nutriente_K']]
y = df_treinamento['Irrigacao']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

modelo = LogisticRegression()
modelo.fit(X_scaled, y)

# Dashboard
st.title("FarmTech Solutions - Irrigação Inteligente")

# Menu de navegação
opcao = st.selectbox("Escolha uma opção", ("Dados de Sensores", "Previsão do Tempo", "Previsão de Irrigação", "Inserir Dados", "Deletar Dados"))

# Exibindo conteúdo baseado na escolha do menu
if opcao == "Dados de Sensores":
    # Exibindo dados de sensores
    dados = obter_dados()
    df = pd.DataFrame(dados, columns=["ID", "Data", "Umidade", "pH", "Nutriente P", "Nutriente K", "Irrigação"])
    st.dataframe(df)
    st.line_chart(df[["Umidade", "pH"]])

elif opcao == "Previsão do Tempo":
    # Previsão do tempo
    cidade = st.text_input("Digite o nome da cidade para a previsão do tempo:", "São Paulo", key="cidade_input")

    if cidade:
        previsao = obter_previsao_tempo(cidade)
        if "Erro" not in previsao:
            st.subheader(f"Previsão do Tempo para {cidade.capitalize()}:")
            for chave, valor in previsao.items():
                st.write(f"{chave}: {valor}")
        else:
            st.error(previsao["Erro"])

elif opcao == "Previsão de Irrigação":
    # Previsão do modelo de irrigação
    st.subheader("Previsão do Modelo de Irrigação")

    umidade_input = st.number_input("Umidade (%)", min_value=0, max_value=100, value=60, key="umidade_input")
    ph_input = st.number_input("pH", min_value=0.0, max_value=14.0, value=6.5, key="ph_input")
    nutriente_p_input = st.selectbox("Nutriente P", ("Adequado", "Inadequado"))
    nutriente_k_input = st.selectbox("Nutriente K", ("Adequado", "Inadequado"))

    # Mapear as opções para valores numéricos
    nutriente_p_valor = 1 if nutriente_p_input == "Adequado" else 0
    nutriente_k_valor = 1 if nutriente_k_input == "Adequado" else 0

    irrigacao_input = st.selectbox
    irrigacao_valor = 1 if irrigacao_input == "Ligada" else 0

    if st.button("Prever Irrigação"):
        resultado = previsao_irrigaçao(modelo, scaler, umidade_input, ph_input, nutriente_p_valor, nutriente_k_valor)
        st.write(resultado)

elif opcao == "Inserir Dados":
    # Inserção de dados
    st.subheader("Inserir Dados no Banco de Dados")

    umidade_input = st.number_input("Umidade (%)", min_value=0, max_value=100, value=60)
    ph_input = st.number_input("pH", min_value=0.0, max_value=14.0, value=6.5)
    
    nutriente_p_input = st.selectbox("Nutriente P", ("Adequado", "Inadequado"))
    nutriente_k_input = st.selectbox("Nutriente K", ("Adequado", "Inadequado"))

   

    irrigacao_input = st.selectbox("Irrigação", ("Ligada", "Desligada"))
    

    if st.button("Inserir Dados"):
        inserir_dados(umidade_input, ph_input, nutriente_p_input, nutriente_k_input, irrigacao_input)
        st.success("Dados inseridos com sucesso!")

elif opcao == "Deletar Dados":
    # Deletar dados
    st.subheader("Deletar Dados do Banco de Dados")
    
    id_dado_input = st.number_input("Digite o ID do dado para deletar", min_value=1, value=1)
    
    if st.button("Deletar Dados"):
        deletar_dado(id_dado_input)
        st.success(f"Dado com ID {id_dado_input} deletado com sucesso!")
