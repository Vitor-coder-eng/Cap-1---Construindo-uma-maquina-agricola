![logo FIAP](https://github.com/Vitor-coder-eng/Cap-1---Construindo-uma-maquina-agricola/blob/main/logo-fiap.png)

# Fase 3: Cap 1 - Construindo uma máquina agrícola

## Projeto de Irrigação Inteligente

### Descrição do Projeto
Este projeto consiste em um sistema de irrigação inteligente, onde o usuário pode monitorar e controlar a irrigação com base em dados de sensores. O sistema utiliza um ESP32 para ler os dados dos sensores e um banco de dados Oracle para armazenar e consultar as leituras dos sensores.

### Lógica do Sistema
O sistema coleta dados de sensores de umidade, pH, e nutrientes (P e K) e armazena essas informações em um banco de dados Oracle. Com base nesses dados, uma previsão de irrigação é feita utilizando um modelo de machine learning que determina se a bomba de irrigação deve ser ligada ou desligada.

### Especificidades do Projeto
- **ESP32**: Utiliza um microcontrolador ESP32 para ler os dados dos sensores.
- **Banco de Dados Oracle**: O sistema armazena os dados dos sensores em um banco de dados Oracle e permite consultas para análise e previsão.
- **Modelo de Machine Learning**: Um modelo de classificação é utilizado para prever se a irrigação deve ser ligada ou desligada com base nos dados.

### Como Funciona
- O usuário pode inserir dados no sistema, como valores de umidade, pH e nutrientes, e o modelo de machine learning faz uma previsão de irrigação.
- O sistema exibe os dados e a previsão para o usuário em tempo real através de uma interface com o Streamlit.

### Arquivos do Projeto
- **Código ESP32**: [Código do ESP32 em C/C++](https://github.com/Vitor-coder-eng/Cap-1---Construindo-uma-maquina-agricola/blob/main/C%C3%B3digo%20do%20ESP32%20em%20CC%2B%2B.txt)
- **Código Python**: [Código Python para banco de dados Oracle e previsão de irrigação](https://github.com/Vitor-coder-eng/Cap-1---Construindo-uma-maquina-agricola/blob/main/dashboard.py)
### Imagem do Circuito ![Imagem do circuito no Wokwi](https://github.com/Vitor-coder-eng/Cap-1---Construindo-uma-maquina-agricola/blob/main/Circuito%20de%20Irriga%C3%A7%C3%A3o%20inteligente.png)

### Demonstração
Veja o vídeo de demonstração do funcionamento completo do projeto no YouTube: [Vídeo de Demonstração](https://youtu.be/SS_aYzK8PSc?si=JFLgnEQ_4eK93Z0Q)

### Como Executar
1. Clone este repositório: `git clone https://github.com/Vitor-coder-eng/Cap-1---Construindo-uma-maquina-agricola`
2. Instale as dependências do Python: `pip install -r requirements.txt`
3. Carregue o código no ESP32 e conecte os sensores.
4. Execute o código Python para interagir com o banco de dados e prever a irrigação.
