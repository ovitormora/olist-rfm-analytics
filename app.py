import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração do layout
st.set_page_config(page_title="Análise RFM - Olist",layout="wide") 

# Carregamento de dados (Com cache para performance) 
@st.cache_data
def carregar_dados(): 
    try:
        return pd.read_csv(os.path.join('data','processed','rfm_final.csv'))
    except FileNotFoundError:
        return None

# Início do App
df = carregar_dados() 

if df is None:
    st.error("Erro: Arquivo de dados não encontrado")
    st.stop()
else:
    # Sidebar (Menu Lateral)
    st.sidebar.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=50) # Logo genérico
    st.sidebar.title("Filtros")

    # Filtro de Segmento
    todos_segmentos = df['Segmento'].unique().tolist()
    segmentos_selecionados = st.sidebar.multiselect(
        "Selecione os segmentos", options=todos_segmentos, default=todos_segmentos
    )

    # Filtro DataFrame
    df_filtrado = df[df['Segmento'].isin(segmentos_selecionados)]

    # Corpo principal 
    st.title("Painel de Segmentação de Clientes")
    st.markdown("Use este painel para identificar oportunidades de marketing e extrair listas de clientes")

    # 1. KPI de indicadores 
    col1, col2, col3 = st.columns(3)

    total_clientes = df_filtrado.shape[0] 
    media_recencia = df_filtrado['recency'].mean()
    media_ticket = df_filtrado['monetary'].mean()

    col1.metric("Clientes Filtrados", f"{total_clientes:,.0f}")
    col2.metric("Média de Recência (Dias)", f"{media_recencia:.1f}")
    col3.metric("Ticket Médio (Lifetime)", f"R$ {media_ticket:.2f}")

    st.divider()

    # 2. Graficos
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Distribuição dos Segmentos") 
        # Contagem por segmento
        contagem = df_filtrado['Segmento'].value_counts().reset_index() 
        contagem.columns = ['Segmento','Clientes'] 
         
        fig_bar = px.bar( 
            contagem, 
            x = 'Segmento', 
            y = 'Clientes', 
            color = 'Segmento', 
            text = 'Clientes', 
            title = 'Distribuição de Clientes por Segmento'
        ) 

        st.plotly_chart(fig_bar, use_container_width=True)

    with col_graf2:
        st.subheader("Scatter Plot: Recencia VS Monetário")
        df_sample = df_filtrado.sample(min(5000, len(df_filtrado))) 

        fig_scatter = px.scatter(
            df_sample, 
            x = "recency", 
            y = "monetary", 
            color = "Segmento", 
            hover_data = ['customer_unique_id'],
            log_y=True
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # 3. Análise de dados detalhada (Boxplots)
    st.subheader('Perfil comportamental por Segmento') 
    aba1, aba2 = st.tabs(['Recencia (Dias sem comprar)','Frequencia (Total de compras)']) 

    with aba1:
        fig_box_r = px.box(
            df_filtrado,
            x='Segmento',
            y='recency',
            color='Segmento',
            title='Distribuição de Recência por Segmento'
        )
        st.plotly_chart(fig_box_r, use_container_width=True)

    with aba2:
        fig_box_f = px.box(
            df_filtrado, 
            x= 'Segmento', 
            y= 'frequency', 
            color='Segmento',
            title='Distribuição de Frequência por Segmento'
        )
        fig_box_f.update_layout(yaxis_range=[0,10])
        st.plotly_chart(fig_box_f, use_container_width=True)

    # 4. Exportação de Dados (A parte "Ação")
    st.divider()
    st.subheader("📥 Exportar Lista para Marketing")
    st.write("Baixe a lista dos clientes filtrados acima para usar em campanhas de e-mail/SMS.")
    
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Baixar CSV Filtrado",
        data=csv,
        file_name='lista_marketing_rfm.csv',
        mime='text/csv',
    )