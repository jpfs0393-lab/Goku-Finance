import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Configuração da página móvel
st.set_page_config(
    page_title="Goku Control - Finanças Z",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS personalizada (Tema Escuro Dragon Ball Z)
st.markdown("""
<style>
    .main { background-color: #0F172A; }
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    
    .card-kpi {
        background: #1E293B;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #334155;
    }
    .card-title {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .card-value {
        font-size: 18px;
        font-weight: bold;
    }
    
    .goku-box {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        border: 2px solid #FF6B00;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        color: #F8FAFC;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(255,107,0,0.25);
    }
</style>
""", unsafe_allow_html=True)

# Função para adicionar meses
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, 28)
    return datetime.date(year, month, day)

# Inicialização do banco de dados na sessão (Dados de Exemplo)
if 'lancamentos' not in st.session_state:
    st.session_state['lancamentos'] = pd.DataFrame([
        {"Data": datetime.date(2026, 10, 1), "Descrição": "Salário Mensal", "Tipo": "Entrada (Receita)", "Bloco": "💼 Entradas", "Valor": 1800.00, "Categoria": "💼 Salário", "Pagamento": "Transferência / MB WAY", "Status": "Pago / Recebido 🟩", "Parcela": "1/1"},
        {"Data": datetime.date(2026, 10, 2), "Descrição": "Renda da Casa", "Tipo": "Saída (Despesa)", "Bloco": "🏠 Gastos Fixos", "Valor": 650.00, "Categoria": "🏠 Habitação", "Pagamento": "Transferência / MB WAY", "Status": "Pago / Recebido 🟩", "Parcela": "1/1"},
        {"Data": datetime.date(2026, 10, 5), "Descrição": "Conta da Luz & Água", "Tipo": "Saída (Despesa)", "Bloco": "🏠 Gastos Fixos", "Valor": 95.00, "Categoria": "⚡ Contas Fixas", "Pagamento": "Débito Direto", "Status": "Pago / Recebido 🟩", "Parcela": "1/1"},
        {"Data": datetime.date(2026, 10, 10), "Descrição": "Supermercado Mensal", "Tipo": "Saída (Despesa)", "Bloco": "🛒 Gastos Variáveis", "Valor": 220.00, "Categoria": "🛒 Alimentação", "Pagamento": "Cartão de Débito", "Status": "Pago / Recebido 🟩", "Parcela": "1/1"},
        {"Data": datetime.date(2026, 10, 15), "Descrição": "Compra de Telemóvel", "Tipo": "Saída (Despesa)", "Bloco": "🛒 Gastos Variáveis", "Valor": 50.00, "Categoria": "📱 Tecnologia", "Pagamento": "Cartão de Crédito", "Status": "Pendente / A Pagar 🟥", "Parcela": "1/10"},
    ])

# Cabeçalho do App
st.markdown("<h2 style='text-align: center; color: #FF6B00; margin-bottom: 0;'>⚡ GOKU CONTROL</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 13px;'>Gestão Financeira com Poder de Super Saiyajin</p>", unsafe_allow_html=True)

# Filtro de Mês no Topo
col_mes, col_ano = st.columns(2)
meses_nome = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
agora = datetime.date.today()

with col_mes:
    mes_sel_nome = st.selectbox("📅 Mês", meses_nome, index=agora.month - 1)
    mes_sel_num = meses_nome.index(mes_sel_nome) + 1

with col_ano:
    ano_sel = st.selectbox("📆 Ano", [2025, 2026, 2027], index=1)

# Filtrar dados pelo mês/ano selecionado
df_completo = st.session_state['lancamentos']
if not df_completo.empty:
    df_completo['Data'] = pd.to_datetime(df_completo['Data'])
    mask = (df_completo['Data'].dt.month == mes_sel_num) & (df_completo['Data'].dt.year == ano_sel)
    df_mes = df_completo[mask].copy()
else:
    df_mes = pd.DataFrame()

# Cálculos KPIs
total_entradas = df_mes[df_mes['Tipo'] == 'Entrada (Receita)']['Valor'].sum() if not df_mes.empty else 0.0
total_saidas = df_mes[df_mes['Tipo'] == 'Saída (Despesa)']['Valor'].sum() if not df_mes.empty else 0.0
saldo = total_entradas - total_saidas
taxa_poupanca = (saldo / total_entradas) if total_entradas > 0 else 0

st.markdown("---")

# Cards KPI
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f'<div class="card-kpi"><div class="card-title">🟢 ENTRADAS</div><div class="card-value" style="color: #10B981;">€{total_entradas:,.2f}</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="card-kpi"><div class="card-title">🔴 SAÍDAS</div><div class="card-value" style="color: #EF4444;">€{total_saidas:,.2f}</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="card-kpi"><div class="card-title">💰 SALDO</div><div class="card-value" style="color: #F59E0B;">€{saldo:,.2f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Goku Reativo (Transformações e Níveis de Poder)
if total_entradas == 0:
    goku_titulo = "⚪ MEDITAÇÃO Z"
    goku_desc = "Sem movimentações registadas para este mês."
    goku_emoji = "🧘‍♂️"
elif taxa_poupanca >= 0.30:
    goku_titulo = "🌌 INSTINTO SUPERIOR"
    goku_desc = "Poder divino! Economizou mais de 30% das suas receitas este mês! 🔥"
    goku_emoji = "🌌"
elif taxa_poupanca >= 0.15:
    goku_titulo = "⚡ SUPER SAIYAJIN BLUE"
    goku_desc = "Excelente ritmo! Poupança entre 15% e 30%. Suas finanças estão invencíveis!"
    goku_emoji = "⚡"
elif taxa_poupanca >= 0.05:
    goku_titulo = "🔥 KAIO-KEN ATIVADO"
    goku_desc = "Bom controlo! Economia entre 5% e 15%. Mantenha o foco!"
    goku_emoji = "🔥"
elif taxa_poupanca >= 0:
    goku_titulo = "🩹 GOKU CANSADO"
    goku_desc = "Sua economia ficou abaixo de 5%. Cuidado para não ficar no vermelho!"
    goku_emoji = "🩹"
else:
    goku_titulo = "😵 KI ESGOTADO"
    goku_desc = "Atenção Guerreiro Z! Gastou mais do que recebeu este mês. Hora de cortar custos!"
    goku_emoji = "😵"

st.markdown(f"""
    <div class="goku-box">
        <h1 style="font-size: 42px; margin: 0;">{goku_emoji}</h1>
        <h3 style="color: #FF6B00; margin-top: 5px; margin-bottom: 5px;">{goku_titulo}</h3>
        <p style="font-size: 14px; margin-bottom: 5px;">{goku_desc}</p>
        <span style="font-size: 12px; color: #94A3B8;">Taxa de Poupança: <b>{taxa_poupanca*100:.1f}%</b></span>
    </div>
""", unsafe_allow_html=True)

# Abas do aplicativo
aba1, aba2, aba3 = st.tabs(["➕ Novo Lançamento", "📋 Extrato do Mês", "📊 Gráficos Z"])

# ABA 1: Form de Novo Lançamento (com Parcelamento Automático)
with aba1:
    st.subheader("Registar Nova Transação")
    with st.form("form_transacao", clear_on_submit=True):
        desc = st.text_input("Descrição (Ex: Supermercado, Aluguer, Compra TV...)")
        
        tipo = st.radio("Tipo de Transação", ["Saída (Despesa)", "Entrada (Receita)"], horizontal=True)
        
        col_bloco, col_cat = st.columns(2)
        with col_bloco:
            bloco = st.selectbox("Bloco / Categoria Geral", [
                "💼 Entradas", "🏠 Gastos Fixos", "🛒 Gastos Variáveis", "📈 Investimentos / Poupança"
            ])
        with col_cat:
            categoria = st.selectbox("Categoria Específica", [
                "💼 Salário / Vale", "🚀 Renda Extra", "🏠 Habitação", "⚡ Contas Fixas",
                "🛒 Alimentação", "🚗 Transporte", "🍔 Lazer", "🏥 Saúde", "📱 Tecnologia", "📈 Reserva / Ações"
            ])
            
        col_v, col_p = st.columns(2)
        with col_v:
            valor = st.number_input("Valor (€)", min_value=0.01, step=1.0)
        with col_p:
            pagamento = st.selectbox("Forma de Pagamento", [
                "Transferência / MB WAY", "Cartão de Débito", "Cartão de Crédito", "Dinheiro", "Débito Direto"
            ])
            
        col_d, col_parc = st.columns(2)
        with col_d:
            data_ini = st.date_input("Data da 1ª Parcela", datetime.date.today())
        with col_parc:
            num_parcelas = st.number_input("Nº de Parcelas", min_value=1, max_value=24, value=1)
            
        status_ini = st.selectbox("Status Atual", ["Pago / Recebido 🟩", "Pendente / A Pagar 🟥"])

        submitted = st.form_submit_button("🚀 Gravar Transação")
        
        if submitted and desc:
            novos_registos = []
            valor_parcela = valor / num_parcelas if num_parcelas > 1 else valor
            
            for i in range(int(num_parcelas)):
                data_parc = add_months(data_ini, i)
                status_parc = status_ini if i == 0 else "Pendente / A Pagar 🟥"
                rotulo_parc = f"{i+1}/{int(num_parcelas)}"
                
                novos_registos.append({
                    "Data": data_parc,
                    "Descrição": desc if num_parcelas == 1 else f"{desc} ({rotulo_parc})",
                    "Tipo": tipo,
                    "Bloco": bloco,
                    "Valor": valor_parcela,
                    "Categoria": categoria,
                    "Pagamento": pagamento,
                    "Status": status_parc,
                    "Parcela": rotulo_parc
                })
                
            df_novos = pd.DataFrame(novos_registos)
            st.session_state['lancamentos'] = pd.concat([st.session_state['lancamentos'], df_novos], ignore_index=True)
            st.success(f"Sucesso! {num_parcelas} registo(s) gravado(s) automaticamente nos meses correspondentes.")
            st.rerun()

# ABA 2: Extrato do Mês
with aba2:
    st.subheader(f"Extrato: {mes_sel_nome} de {ano_sel}")
    
    if not df_mes.empty:
        # Formatação para exibição
        df_exibir = df_mes[['Data', 'Descrição', 'Bloco', 'Valor', 'Status', 'Pagamento']].copy()
        df_exibir['Data'] = df_exibir['Data'].dt.strftime('%d/%m/%Y')
        
        st.dataframe(df_exibir, use_container_width=True)
        
        st.markdown("---")
        st.caption("💡 Para alterar o status de pago/pendente ou apagar registos, limpe os dados abaixo se necessário.")
        if st.button("🗑️ Limpar Todos os Registos do Sistema"):
            st.session_state['lancamentos'] = pd.DataFrame(columns=["Data", "Descrição", "Tipo", "Bloco", "Valor", "Categoria", "Pagamento", "Status", "Parcela"])
            st.rerun()
    else:
        st.info("Nenhum lançamento encontrado para o mês selecionado.")

# ABA 3: Gráficos Visuais
with aba3:
    st.subheader("Análise Visual de Gastos")
    
    if not df_mes.empty and total_saidas > 0:
        df_saidas = df_mes[df_mes['Tipo'] == 'Saída (Despesa)']
        
        # Gráfico por Bloco
        fig_bloco = px.pie(
            df_saidas, 
            names='Bloco', 
            values='Valor', 
            hole=0.4,
            title="Distribuição de Saídas por Bloco",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_bloco, use_container_width=True)
        
        # Gráfico por Forma de Pagamento
        fig_pag = px.pie(
            df_saidas, 
            names='Pagamento', 
            values='Valor', 
            hole=0.4,
            title="Gastos por Forma de Pagamento",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pag, use_container_width=True)
    else:
        st.info("Adicione despesas neste mês para visualizar os gráficos de rosca.")
