import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora UFRGS 2026",
    layout="centered",
    page_icon="🎓"
)

# --- CABEÇALHO ---
st.title("Calculadora Média Harmônica UFRGS 2026")

st.warning("⚠️ **Atenção:** O cálculo abaixo utiliza os **pesos específicos para o curso de MEDICINA**.")

st.info(
    "ℹ️ **Dados Atualizados:** Médias e desvios padrão baseados no gabarito oficial preliminar, "
    "conforme dados extraídos do site da UFRGS em **01/12/2025**."
)

st.divider()

# --- DADOS ESTATÍSTICOS OFICIAIS (FONTE: UFRGS CV2026 PRELIMINAR) ---
# Estrutura: {Disciplina: {media, desvio, peso}}
dados_fixos = {
    "Física":           {"media": 5.6696, "desvio": 2.7158, "peso": 1},
    "Literatura":       {"media": 8.1423, "desvio": 3.2892, "peso": 1},
    "Língua Portuguesa":{"media": 8.9877, "desvio": 2.3580, "peso": 3},
    "Biologia":         {"media": 6.1949, "desvio": 2.6064, "peso": 3},
    "Química":          {"media": 5.2824, "desvio": 2.4953, "peso": 2},
    "Geografia":        {"media": 5.8837, "desvio": 2.2946, "peso": 1},
    "História":         {"media": 7.9046, "desvio": 2.9607, "peso": 1},
    "Matemática":       {"media": 5.3712, "desvio": 3.2690, "peso": 1},
}

# --- INTERFACE DE ENTRADA ---
st.subheader("Informe seu número de acertos")
st.caption("Insira quantos acertos você teve em cada prova (de 0 a 25).")

opcao_lingua = st.radio("Qual sua Língua Estrangeira?", ("Inglês", "Espanhol"))

# Configuração da língua estrangeira com dados 2026
if opcao_lingua == "Inglês":
    dados_prova = dados_fixos.copy()
    dados_prova["Inglês"] = {"media": 5.0184, "desvio": 2.7347, "peso": 2}
else:
    dados_prova = dados_fixos.copy()
    dados_prova["Espanhol"] = {"media": 5.7125, "desvio": 2.2755, "peso": 2}

# Ordem de exibição tradicional
ordem_exibicao = [
    "Física", "Literatura", opcao_lingua, "Língua Portuguesa", 
    "Biologia", "Química", "Geografia", "História", "Matemática"
]

acertos = {}
col1, col2 = st.columns(2)

for i, disciplina in enumerate(ordem_exibicao):
    with col1 if i % 2 == 0 else col2:
        acertos[disciplina] = st.number_input(
            label=disciplina,
            min_value=0, 
            max_value=25, 
            value=15,
            step=1
        )

# --- CÁLCULO ---
if st.button("Calcular Média Final", type="primary"):
    soma_pesos = 0
    soma_peso_sobre_ep = 0
    detalhes_calculo = []
    
    for disciplina in ordem_exibicao:
        n_acertos = acertos[disciplina]
        dados = dados_prova[disciplina]
        
        # 1. Cálculo do Escore Padronizado (EP)
        # Fórmula: 500 + 100 * ((Acertos - Média) / Desvio)
        # Se desvio for zero (improvável no vestibular), evita divisão por zero
        if dados['desvio'] == 0:
            ep = 500
        else:
            ep = 500 + 100 * ((n_acertos - dados['media']) / dados['desvio'])
        
        # O Escore Padronizado nunca é negativo nas regras da UFRGS, mas matematicamente pode ocorrer
        # se o aluno for muito mal. O cálculo segue a fórmula matemática pura.
        
        # 2. Termo da Média Harmônica: Peso / EP
        # Evitar divisão por zero se EP for muito baixo (teoricamente possível)
        if ep <= 0:
            ep = 0.1 # Proteção matemática simples
            
        termo = dados['peso'] / ep
        
        soma_pesos += dados['peso']
        soma_peso_sobre_ep += termo
        
        detalhes_calculo.append({
            "Disciplina": disciplina, 
            "Acertos": n_acertos, 
            "Escore (EP)": round(ep, 2),
            "Peso": dados['peso']
        })
        
    # Cálculo final da Média Harmônica
    # MH = Soma dos Pesos / Soma (Peso/EP)
    media_harmonica = soma_pesos / soma_peso_sobre_ep
    
    # --- EXIBIÇÃO DOS RESULTADOS ---
    st.divider()
    st.markdown(f"### 🎯 Média Harmônica Final: `{media_harmonica:.2f}`")
    
    with st.expander("Ver tabela detalhada de escores"):
        df = pd.DataFrame(detalhes_calculo)
        st.dataframe(
            df.style.format({"Escore (EP)": "{:.2f}"}), 
            use_container_width=True
        )

    st.markdown("---")
    st.caption("Desenvolvido para auxiliar vestibulandos de Medicina da UFRGS.")