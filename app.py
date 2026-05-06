import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard EPAS-Huíla", layout="wide")

st.title("📊 Dashboard - Infraestrutura de TI EPAS-Huíla")
st.markdown("Análise dos dados do questionário (Amostra: 17 participantes)")

# ---------------------------
# Dados
# ---------------------------

data_os = pd.DataFrame({
    "Sistema": ["Windows Server", "Linux", "Outros"],
    "Quantidade": [11, 4, 2]
})

data_virtualizacao = pd.DataFrame({
    "Tecnologia": ["VMware", "Hyper-V", "KVM", "Não utilizam"],
    "Quantidade": [5, 3, 1, 8]
})

data_servicos = pd.DataFrame({
    "Serviço": ["Internet", "Email", "Partilha de Arquivos", "VPN"],
    "Quantidade": [17, 12, 10, 3]
})

data_segurança = pd.DataFrame({
    "Medida": ["Firewall", "Antivírus", "Políticas de Acesso", "IDS", "Criptografia"],
    "Quantidade": [13, 15, 9, 4, 3]
})

data_desafios = pd.DataFrame({
    "Desafio": ["Desempenho lento", "Falhas nos servidores", "Vulnerabilidades", "Gestão difícil", "Acesso remoto"],
    "Quantidade": [12, 9, 11, 10, 8]
})

data_necessidades = pd.DataFrame({
    "Necessidade": ["Segurança", "Desempenho", "Gestão", "Acesso remoto", "Disponibilidade"],
    "Quantidade": [14, 13, 11, 12, 10]
})

data_aceitacao = pd.DataFrame({
    "Opinião": ["Muito favorável", "Favorável", "Neutro"],
    "Quantidade": [7, 8, 2]
})

# ---------------------------
# Função para gráfico
# ---------------------------
def plot_chart(df, x, y, title):
    fig, ax = plt.subplots()
    ax.bar(df[x], df[y])
    ax.set_title(title)
    ax.set_ylabel("Quantidade")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ---------------------------
# Layout
# ---------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("💻 Sistemas Operacionais")
    plot_chart(data_os, "Sistema", "Quantidade", "Sistemas Operacionais")

    st.subheader("🖥️ Virtualização")
    plot_chart(data_virtualizacao, "Tecnologia", "Quantidade", "Uso de Virtualização")

    st.subheader("🌐 Serviços de Rede")
    plot_chart(data_servicos, "Serviço", "Quantidade", "Serviços Disponíveis")

with col2:
    st.subheader("🔐 Segurança")
    plot_chart(data_segurança, "Medida", "Quantidade", "Medidas de Segurança")

    st.subheader("⚠️ Desafios")
    plot_chart(data_desafios, "Desafio", "Quantidade", "Principais Desafios")

    st.subheader("📈 Necessidades")
    plot_chart(data_necessidades, "Necessidade", "Quantidade", "Necessidades Identificadas")

# ---------------------------
# Aceitação (Destaque)
# ---------------------------
st.subheader("✅ Aceitação da Solução (Linux + VPN)")
plot_chart(data_aceitacao, "Opinião", "Quantidade", "Nível de Aceitação")

# ---------------------------
# Insights
# ---------------------------
st.markdown("## 📌 Principais Insights")

st.info("""
- A maioria utiliza Windows Server, mas há espaço para Linux.
- Quase metade não usa virtualização.
- VPN é pouco utilizada → problema de acesso remoto.
- Segurança ainda é básica (pouca criptografia e IDS).
- Forte aceitação da solução proposta (mais de 80% favorável).
""")

# ---------------------------
# Rodapé
# ---------------------------
st.markdown("---")
st.caption("Desenvolvido para análise do TCC - EPAS-Huíla")