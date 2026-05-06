import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Dashboard EPAS-Huíla",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Page background */
.stApp {
    background-color: #f5f4f0;
}

/* Remove default padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Header strip */
.header-block {
    background: #0f1923;
    border-radius: 14px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-title {
    font-size: 22px;
    font-weight: 600;
    color: #f0ede6;
    margin: 0;
    letter-spacing: -0.3px;
}
.header-sub {
    font-size: 13px;
    color: #8a8f96;
    margin: 4px 0 0;
}
.header-badge {
    background: #1e2d3d;
    color: #5ba3d9;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid #2a3f55;
}

/* Metric cards */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.metric-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 20px 22px;
    border: 1px solid #e8e5de;
}
.metric-label {
    font-size: 11px;
    font-weight: 500;
    color: #9a9690;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 8px;
}
.metric-value {
    font-size: 32px;
    font-weight: 600;
    color: #0f1923;
    margin: 0;
    line-height: 1;
    font-family: 'DM Mono', monospace;
}
.metric-note {
    font-size: 12px;
    color: #b0ada6;
    margin: 6px 0 0;
}
.metric-accent-blue  { border-left: 3px solid #3b7dd8; }
.metric-accent-teal  { border-left: 3px solid #1d9e75; }
.metric-accent-amber { border-left: 3px solid #d48b0f; }
.metric-accent-green { border-left: 3px solid #3d9a50; }

/* Chart card */
.chart-card-title {
    font-size: 11px;
    font-weight: 500;
    color: #9a9690;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 2px;
}

/* Acceptance bar */
.accept-container {
    background: #ffffff;
    border-radius: 12px;
    padding: 22px 26px;
    border: 1px solid #e8e5de;
    margin-bottom: 20px;
}
.accept-title {
    font-size: 11px;
    font-weight: 500;
    color: #9a9690;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 16px;
}
.accept-blocks {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 10px;
    margin-bottom: 14px;
}
.accept-block {
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.accept-block-pct  { font-size: 28px; font-weight: 600; margin: 0; font-family: 'DM Mono', monospace; }
.accept-block-lbl  { font-size: 12px; margin: 4px 0 0; }
.accept-block-n    { font-size: 11px; margin: 2px 0 0; opacity: 0.65; }
.accept-bar        { height: 8px; border-radius: 4px; overflow: hidden; display: flex; gap: 3px; }
.accept-bar-green  { background: #3d9a50; border-radius: 4px 0 0 4px; }
.accept-bar-blue   { background: #3b7dd8; }
.accept-bar-gray   { background: #ddd9d0; border-radius: 0 4px 4px 0; flex: 1; }

/* Insights */
.insight-card {
    background: #0f1923;
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 20px;
}
.insight-title {
    font-size: 13px;
    font-weight: 600;
    color: #f0ede6;
    margin: 0 0 12px;
}
.insight-item {
    font-size: 13px;
    color: #8a8f96;
    margin: 0 0 8px;
    padding-left: 14px;
    position: relative;
    line-height: 1.6;
}
.insight-item::before {
    content: '→';
    position: absolute;
    left: 0;
    color: #3b7dd8;
}
.insight-item strong { color: #c8e2f8; }

/* Footer */
.footer {
    text-align: center;
    font-size: 12px;
    color: #b0ada6;
    padding-top: 16px;
    border-top: 1px solid #e8e5de;
    margin-top: 8px;
}

/* Plotly chart background fix */
.js-plotly-plot .plotly .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Paleta de cores Plotly ────────────────────────────────────────────────────
BLUE   = "#3b7dd8"
TEAL   = "#1d9e75"
AMBER  = "#d48b0f"
CORAL  = "#c94f2e"
PURPLE = "#6f67c9"
GRAY   = "#9a9690"
BG     = "#ffffff"
TEXT   = "#0f1923"
GRID   = "rgba(0,0,0,0.05)"

LAYOUT_BASE = dict(
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font=dict(family="DM Sans, sans-serif", color=TEXT, size=12),
    margin=dict(l=8, r=8, t=8, b=8),
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11, color=GRAY)),
    yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(size=11, color=GRAY)),
)

def layout(**kwargs):
    d = dict(LAYOUT_BASE)
    d.update(kwargs)
    return d

# ── Dados ─────────────────────────────────────────────────────────────────────
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

data_seguranca = pd.DataFrame({
    "Medida": ["Antivírus", "Firewall", "Políticas de Acesso", "IDS", "Criptografia"],
    "Quantidade": [15, 13, 9, 4, 3]
})

data_desafios = pd.DataFrame({
    "Desafio": ["Desempenho lento", "Vulnerabilidades", "Gestão difícil", "Falhas servidores", "Acesso remoto"],
    "Quantidade": [12, 11, 10, 9, 8]
})

data_necessidades = pd.DataFrame({
    "Necessidade": ["Segurança", "Desempenho", "Acesso remoto", "Gestão", "Disponibilidade"],
    "Quantidade": [14, 13, 12, 11, 10]
})

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
  <div>
    <p class="header-title">🖥️ Dashboard — Infraestrutura de TI EPAS-Huíla</p>
    <p class="header-sub">Análise do questionário aplicado na instituição</p>
  </div>
  <span class="header-badge">n = 17 participantes</span>
</div>
""", unsafe_allow_html=True)

# ── Metric Cards ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-row">
  <div class="metric-card metric-accent-blue">
    <p class="metric-label">Windows Server</p>
    <p class="metric-value">65%</p>
    <p class="metric-note">11 de 17 servidores</p>
  </div>
  <div class="metric-card metric-accent-amber">
    <p class="metric-label">Sem virtualização</p>
    <p class="metric-value">47%</p>
    <p class="metric-note">8 unidades afetadas</p>
  </div>
  <div class="metric-card metric-accent-teal">
    <p class="metric-label">VPN em uso</p>
    <p class="metric-value">18%</p>
    <p class="metric-note">Apenas 3 de 17</p>
  </div>
  <div class="metric-card metric-accent-green">
    <p class="metric-label">Aceitação favorável</p>
    <p class="metric-value">88%</p>
    <p class="metric-note">Solução Linux + VPN</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Row 1: OS + Virtualização ─────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown('<p class="chart-card-title">💻 Sistemas Operacionais</p>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=data_os["Sistema"],
        y=data_os["Quantidade"],
        marker_color=[BLUE, TEAL, GRAY],
        marker_line_width=0,
        width=0.55,
        text=data_os["Quantidade"],
        textposition="outside",
        textfont=dict(size=13, color=TEXT, family="DM Mono, monospace"),
    ))
    fig.update_layout(**layout(yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                                           tickfont=dict(size=11, color=GRAY), range=[0, 14])))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<p class="chart-card-title">🔄 Virtualização</p>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=data_virtualizacao["Tecnologia"],
        y=data_virtualizacao["Quantidade"],
        marker_color=[BLUE, PURPLE, TEAL, GRAY],
        marker_line_width=0,
        width=0.55,
        text=data_virtualizacao["Quantidade"],
        textposition="outside",
        textfont=dict(size=13, color=TEXT, family="DM Mono, monospace"),
    ))
    fig.update_layout(**layout(yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                                           tickfont=dict(size=11, color=GRAY), range=[0, 11])))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Row 2: Segurança + Desafios ───────────────────────────────────────────────
col3, col4 = st.columns(2, gap="medium")

with col3:
    st.markdown('<p class="chart-card-title">🔐 Medidas de Segurança</p>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        y=data_seguranca["Medida"],
        x=data_seguranca["Quantidade"],
        orientation="h",
        marker_color=PURPLE,
        marker_line_width=0,
        width=0.6,
        text=data_seguranca["Quantidade"],
        textposition="outside",
        textfont=dict(size=12, color=TEXT, family="DM Mono, monospace"),
    ))
    fig.update_layout(**layout(
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickfont=dict(size=11, color=GRAY), range=[0, 18]),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=12, color=TEXT)),
        height=240,
    ))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col4:
    st.markdown('<p class="chart-card-title">⚠️ Principais Desafios</p>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        y=data_desafios["Desafio"],
        x=data_desafios["Quantidade"],
        orientation="h",
        marker_color=CORAL,
        marker_line_width=0,
        width=0.6,
        text=data_desafios["Quantidade"],
        textposition="outside",
        textfont=dict(size=12, color=TEXT, family="DM Mono, monospace"),
    ))
    fig.update_layout(**layout(
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickfont=dict(size=11, color=GRAY), range=[0, 15]),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=12, color=TEXT)),
        height=240,
    ))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Row 3: Necessidades + Serviços ────────────────────────────────────────────
col5, col6 = st.columns([3, 2], gap="medium")

with col5:
    st.markdown('<p class="chart-card-title">📈 Necessidades Identificadas</p>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=data_necessidades["Necessidade"],
        y=data_necessidades["Quantidade"],
        marker_color=[AMBER, AMBER, AMBER, AMBER, AMBER],
        marker_line_width=0,
        width=0.55,
        text=data_necessidades["Quantidade"],
        textposition="outside",
        textfont=dict(size=13, color=TEXT, family="DM Mono, monospace"),
    ))
    fig.update_layout(**layout(yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                                           tickfont=dict(size=11, color=GRAY), range=[0, 17])))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col6:
    st.markdown('<p class="chart-card-title">🌐 Serviços de Rede</p>', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=data_servicos["Serviço"],
        y=data_servicos["Quantidade"],
        marker_color=[TEAL, TEAL, TEAL, CORAL],
        marker_line_width=0,
        width=0.55,
        text=data_servicos["Quantidade"],
        textposition="outside",
        textfont=dict(size=13, color=TEXT, family="DM Mono, monospace"),
    ))
    fig.update_layout(**layout(
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
                   tickfont=dict(size=11, color=GRAY), range=[0, 20]),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11, color=GRAY)),
    ))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Aceitação da Solução ──────────────────────────────────────────────────────
st.markdown("""
<div class="accept-container">
  <p class="accept-title">✅ Aceitação da Solução Proposta (Linux + VPN)</p>
  <div class="accept-blocks">
    <div class="accept-block" style="background:#eaf4ec;">
      <p class="accept-block-pct" style="color:#2a7a3b;">41%</p>
      <p class="accept-block-lbl" style="color:#3d9a50;">Muito favorável</p>
      <p class="accept-block-n" style="color:#3d9a50;">7 participantes</p>
    </div>
    <div class="accept-block" style="background:#e8f0fb;">
      <p class="accept-block-pct" style="color:#1e4f9c;">47%</p>
      <p class="accept-block-lbl" style="color:#3b7dd8;">Favorável</p>
      <p class="accept-block-n" style="color:#3b7dd8;">8 participantes</p>
    </div>
    <div class="accept-block" style="background:#f5f4f0;">
      <p class="accept-block-pct" style="color:#5a5754;">12%</p>
      <p class="accept-block-lbl" style="color:#9a9690;">Neutro</p>
      <p class="accept-block-n" style="color:#b0ada6;">2 participantes</p>
    </div>
  </div>
  <div class="accept-bar">
    <div class="accept-bar-green" style="width:41%;"></div>
    <div class="accept-bar-blue"  style="width:47%;"></div>
    <div class="accept-bar-gray"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Insights ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="insight-card">
  <p class="insight-title">📌 Principais Insights</p>
  <p class="insight-item">Maioria usa <strong>Windows Server (65%)</strong>, mas Linux tem presença real — espaço para migração gradual.</p>
  <p class="insight-item">Quase metade <strong>(47%)</strong> não utiliza virtualização — oportunidade clara de modernização da infraestrutura.</p>
  <p class="insight-item">VPN muito subutilizada <strong>(18%)</strong> apesar do acesso remoto ser um desafio no top 5.</p>
  <p class="insight-item">Segurança ainda básica: criptografia e IDS presentes em <strong>menos de 25%</strong> das unidades.</p>
  <p class="insight-item">Solução proposta com forte aceitação: <strong>88% favorável</strong> ou muito favorável entre os participantes.</p>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<p class="footer">Desenvolvido para análise do TCC — EPAS-Huíla</p>', unsafe_allow_html=True)
