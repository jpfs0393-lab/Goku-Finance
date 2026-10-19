import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Goku Control - Gestão Financeira",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main { background-color: #0F172A; }
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .card-kpi {
        background: #1E293B;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #334155;
    }
    .card-title {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .card-value {
        font-size: 20px;
        font-weight: bold;
    }
    .goku-box {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        border: 2px solid #FF6B00;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        color: #1E293B;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(255,107,0,0.2);
    }
    h1, h2, h3 { color: #F8FAFC !important; }
</style>
""", unsafe_allow_html=True)

if 'lancamentos' not in st.session_state:
    st.session_state['lancamentos'] = pd.DataFrame([
        {"Data": datetime.date(2026, 10, 1), "Descrição": "Salário Mensal", "Tipo": "Receita", "Valor": 1800.00, "Categoria": "💼 Trabalho"},
        {"Data": datetime.date(2026, 10, 2), "Descrição": "Renda / Aluguer", "Tipo": "Despesa", "Valor": 650.00, "Categoria": "🏠 Habitação"},
        {"Data": datetime.date(2026, 10, 3), "Descrição": "Supermercado", "Tipo": "Despesa", "Valor": 180.50, "Categoria": "🛒 Alimentação"},
        {"Data": datetime.date(2026, 10, 5), "Descrição": "Luz e Água", "Tipo": "Despesa", "Valor": 85.00, "Categoria": "⚡ Contas Fixas"},
        {"Data": datetime.date(2026, 10, 10), "Descrição": "Combustível", "Tipo": "Despesa", "Valor": 60.00, "Categoria": "🚗 Transporte"},
    ])

df = st.session_state['lancamentos']

st.markdown("<h2 style='text-align: center; color: #FF6B00;'>⚡ GOKU CONTROL</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14px;'>Seu app financeiro pessoal com poder de Super Saiyajin</p>", unsafe_allow_html=True)
st.markdown("---")

total_receitas = df[df['Tipo'] == 'Receita']['Valor'].sum()
total_despesas = df[df['Tipo'] == 'Despesa']['Valor'].sum()
saldo = total_receitas - total_despesas
taxa_poupanca = (saldo / total_receitas) if total_receitas > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
        <div class="card-kpi">
            <div class="card-title">🟢 ENTRAM</div>
            <div class="card-value" style="color: #10B981;">€{total_receitas:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="card-kpi">
            <div class="card-title">🔴 SAEM</div>
            <div class="card-value" style="color: #EF4444;">€{total_despesas:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="card-kpi">
            <div class="card-title">💰 SOBRA</div>
            <div class="card-value" style="color: #F59E0B;">€{saldo:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if total_receitas == 0:
    goku_titulo = "⚪ AGUARDANDO LANÇAMENTOS"
    goku_desc = "Adicione suas receitas e despesas abaixo para revelar seu nível de poder!"
    goku_emoji = "⚪"
elif taxa_poupanca > 0.3:
    goku_titulo = "🌌 INSTINTO SUPERIOR"
    goku_desc = "Economizou mais de 30%! Poder divino atingido com sucesso! 🔥"
    goku_emoji = "🌌"
elif taxa_poupanca >= 0.15:
    goku_titulo = "⚡ SUPER SAIYAJIN BLUE"
    goku_desc = "Economia entre 15% e 30%. Suas finanças estão invencíveis! 💪"
    goku_emoji = "⚡"
elif taxa_poupanca >= 0.05:
    goku_titulo = "🔥 KAIO-KEN ATIVADO"
    goku_desc = "Economia entre 5% e 15%. Bom ritmo de controle financeiro! 🎯"
    goku_emoji = "🔥"
elif taxa_poupanca >= 0:
    goku_titulo = "🩹 GOKU CANSADO"
    goku_desc = "Economia abaixo de 5%. Precisa urgente de uma Semente dos Deuses! 🌾"
    goku_emoji = "🩹"
else:
    goku_titulo = "😵 KI ESGOTADO"
    goku_desc = "Você gastou mais do que recebeu! Perigo financeiro severo! 🔴"
    goku_emoji = "😵"

st.markdown(f"""
    <div class="goku-box">
        <h1 style="font-size: 40px; margin: 0;">{goku_emoji}</h1>
        <h3 style="color: #C2410C; margin-top: 5px; margin-bottom: 5px;">{goku_titulo}</h3>
        <p style="font-size: 15px; font-weight: 600; color: #1E293B;">{goku_desc}</p>
        <p style="font-size: 12px; color: #64748B; margin-bottom: 0;">Taxa de poupança atual: <b>{taxa_poupanca*100:.1f}%</b></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

aba1, aba2 = st.tabs(["➕ Novo Lançamento", "📋 Extrato do Mês"])

with aba1:
    st.subheader("Registar Nova Transação")
    with st.form("form_transacao", clear_on_submit=True):
        desc = st.text_input("Descrição (Ex: Supermercado, Aluguer...)")
        tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
        valor = st.number_input("Valor (€)", min_value=0.01, step=1.0)
        categoria = st.selectbox("Categoria", [
            "💼 Trabalho", "🚀 Renda Extra", "🏠 Habitação", 
            "⚡ Contas Fixas", "🛒 Alimentação", "🚗 Transporte", "🍔 Lazer", "🏥 Saúde"
        ])
        data_lanc = st.date_input("Data", datetime.date.today())
        
        submitted = st.form_submit_button("🚀 Registar no App")
        if submitted and desc:
            novo_dado = pd.DataFrame([{"Data": data_lanc, "Descrição": desc, "Tipo": tipo, "Valor": valor, "Categoria": categoria}])
            st.session_state['lancamentos'] = pd.concat([st.session_state['lancamentos'], novo_dado], ignore_index=True)
            st.success("Transação registada com sucesso! O poder do Goku foi atualizado.")
            st.rerun()

with aba2:
    st.subheader("Histórico de Movimentos")
    if not df.empty:
        st.dataframe(df.sort_values(by="Data", ascending=False), use_container_width=True)
        if st.button("🗑️ Limpar Todos os Registos"):
            st.session_state['lancamentos'] = pd.DataFrame(columns=["Data", "Descrição", "Tipo", "Valor", "Categoria"])
            st.rerun()
    else:
        st.info("Nenhum lançamento registado ainda.")
