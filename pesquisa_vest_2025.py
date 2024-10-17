import streamlit as st
import pandas as pd
from PIL import Image  # Para carregar a imagem

# Configura a página para o layout wide
st.set_page_config(layout="wide")

# Exibir todas as colunas sem truncar
pd.set_option('display.max_columns', None)  # Exibe todas as colunas
pd.set_option('display.width', 1000)        # Ajusta a largura máxima para exibir colunas

# URL do CSV
url_vestibular = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT45YDXevL7xGBAE7x8CN-7B2cXWN8YtmSN98pEbzpkJhvEY234T0Jp6Ntm9hNZgN9U1Q2ZiiDZG7sS/pub?gid=136567823&single=true&output=csv"

# Função para baixar o CSV e carregar em um DataFrame
def baixar_csv_para_df(url):
    df = pd.read_csv(url)
    return df

# Função para remover pontos e traços do CPF no DataFrame
def limpar_formatacao_cpf(df):
    df['CPF'] = df['CPF'].str.replace(r'[.-]', '', regex=True)
    return df

# Função para formatar o CPF de volta no padrão XXX.XXX.XXX-XX
def formatar_cpf(cpf):
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

# Função para buscar o aluno pelo CPF e retornar as informações na ordem desejada
def buscar_aluno_por_cpf(df, cpf_aluno):
    # Filtra o DataFrame para encontrar o aluno com o CPF informado
    aluno = df[df['CPF'] == cpf_aluno]
    
    # Verifica se o aluno foi encontrado
    if not aluno.empty:
        # Formata o CPF antes de retornar os resultados
        aluno['CPF'] = aluno['CPF'].apply(formatar_cpf)
        # Converte o número de inscrição para inteiro
        aluno['NUMEROINSCRICAO'] = aluno['NUMEROINSCRICAO'].astype(int).astype(str)  # Converte para string após ser inteiro para evitar formatação
        # Retorna as colunas na ordem especificada
        return aluno[['NUMEROINSCRICAO', 'CPF', 'NOME_CANDIDATO', 'LOCAL', 'SALA', 'CURSO']]
    else:
        return "Aluno não encontrado."

# Carregamento inicial do DataFrame
df_vestibular_completo = baixar_csv_para_df(url_vestibular)

# Limpar a formatação do CPF no DataFrame para garantir a busca por números apenas
df_vestibular_completo = limpar_formatacao_cpf(df_vestibular_completo)

# Adicionando CSS personalizado
st.markdown(
    """
    <style>
    .title {
        color: #1a73e8;
        font-size: 36px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 24px;
        text-align: center;
        margin-bottom: 40px;
        color: #555;
    }
    .text-input {
        border: 2px solid #1a73e8;
        border-radius: 5px;
        padding: 10px;
        font-size: 18px;
    }
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
    }
    .centered-image {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;  /* Espaçamento abaixo da imagem */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar a imagem diretamente
img = Image.open('img/ico_vest_25.png')  # Ajuste o caminho se necessário

# Centralizando a imagem
st.markdown("<div class='centered-image'>", unsafe_allow_html=True)
st.image(img, width=200, use_column_width=False)
st.markdown("</div>", unsafe_allow_html=True)

# Título da página
st.markdown("<div class='title'>Busca do candidato por CPF</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Encontre as informações do candidato utilizando o CPF</div>", unsafe_allow_html=True)

# Entrada de CPF - permite somente números
cpf_procurado = st.text_input("Digite o CPF do candidato (somente números):", max_chars=11, key='cpf_input', placeholder="Somente números", help="Digite o CPF sem pontos ou traços.")

# Verificar se o CPF foi inserido
if cpf_procurado:
    # Filtrar e buscar aluno
    aluno_info = buscar_aluno_por_cpf(df_vestibular_completo, cpf_procurado)
    
    # Exibir o resultado
    if isinstance(aluno_info, pd.DataFrame):
        st.write("Informações do aluno:")
        # Resetar o índice e remover o índice original
        aluno_info = aluno_info.reset_index(drop=True)  # Remove o índice original
        
        # Exibir o DataFrame sem índice
        st.dataframe(aluno_info, use_container_width=True)  # use_container_width para melhorar o layout
    else:
        st.error(aluno_info)
