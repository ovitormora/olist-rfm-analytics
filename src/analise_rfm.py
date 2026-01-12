import pandas as pd
import numpy  as np 
import os 

def calcular_rfm_scores():
    print(" --- Implementando Calculo de RFM ---") 

    # 1. Carregamento de dados
    try:
        df_rfm = pd.read_csv(os.path.join('data','processed','rfm_data.csv')) 
        print("Arquivo carregado com sucesso")
    except FileNotFoundError:
        print("Erro: Execute o processamento de dados primeiro") 
        return 

    # 2. Criação de Score (1 - 5)

    # R - Recência (Quanto menor, melhor -> labels invertidos)
    # pd.qcut divide os dados em quantis (partes iguais)
    df_rfm['R_score'] = pd.qcut(df_rfm['recency'], q=5, labels=[5,4,3,2,1])

    # M - Monetário (Quanto maior, melhor -> labels iguais)
    df_rfm['M_score'] = pd.qcut(df_rfm['monetary'], q=5, labels=[1,2,3,4,5]) 

    # F - Frequência (O Desafio dos Empates)
    # Como +90% dos clientes compraram apenas 1 vez, o qcut falha (limites duplicados).
    # Solução: Usamos o método 'rank' primeiro para desempatar aleatoriamente.
    df_rfm['F_score'] = pd.qcut(df_rfm['frequency'].rank(method='first'),q=5,labels=[1,2,3,4,5]) 

    # 3. Criação de String do resultado RFM para facilitar a leitura visual
    df_rfm['RFM_Segment'] = (
        df_rfm['R_score'].astype(str) + df_rfm['F_score'].astype(str) + df_rfm['M_score'].astype(str) 
    )

    # 4. Criação de Score Geral (Soma) axis=1 soma as colunas
    df_rfm['RFM_Score_Total'] = df_rfm[['R_score', 'F_score', 'M_score']].sum(axis=1)


    # 5. Segmentação de Marketing (Regra de Negócio)
    # Função para nomeação

    def segmentar_cliente(row):
        r = row['R_score']
        f = row['F_score']
        
        # Lógica baseada em R (Tempo) e F (Fidelidade)
        if r >= 4 and f >= 4:
            return 'Campeões'          # Comprou recentemente e compra sempre
        elif r >= 4 and f <= 2:
            return 'Promissores/Novos' # Comprou recentemente, mas poucas vezes
        elif r <= 2 and f >= 4:
            return 'Em Risco'          # Comprava muito, mas sumiu (Churn)
        elif r <= 2 and f <= 2:
            return 'Hibernando'        # Comprou faz tempo e pouco
        elif 3 <= r <= 4 and 3 <= f <= 4:
            return 'Leais em Potencial'
        else:
            return 'Precisam de Atenção' # A média

    df_rfm['Segmento'] = df_rfm.apply(segmentar_cliente, axis=1)

    print("--- Distribuição dos Segmentos ---")
    print(df_rfm['Segmento'].value_counts())

    # 6. Salvar Final
    df_rfm.to_csv('data/processed/rfm_final.csv', index=False)
    print("Arquivo final salvo em: data/processed/rfm_final.csv")

if __name__ == "__main__":
    calcular_rfm_scores()
        