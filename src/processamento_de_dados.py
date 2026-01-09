import pandas as pd
import numpy as np  
import os

def carregar_e_processar_dados():
    print("--- Carregando Datasets ---")

    ## Carregando apenas colunas necessarias do CSV para economizar memoria
    # Resolve o caminho absoluto baseado na localização do script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, "..", "data", "raw")
    
    try:
        df_orders = pd.read_csv(
            os.path.join(base_path, 'olist_orders_dataset.csv'),
            usecols=["order_id", "customer_id", "order_purchase_timestamp", "order_status"]
        )

        df_items = pd.read_csv(
            os.path.join(base_path, 'olist_order_items_dataset.csv'),
            usecols=["order_id","price"]
        )

        df_costumer = pd.read_csv(
            os.path.join(base_path, 'olist_customers_dataset.csv'),
            usecols=["customer_id", "customer_unique_id"]
        )

        ## 2.0 Filtragem inicial (Regra de Negócio)
        # Apenas pedidos entregue 'delivered' , pois pedidos cancelados não geram receita
        df_orders = df_orders[df_orders['order_status'] == 'delivered'].copy()

        ## converter data para datetime
        df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])

        ## 3. MERGE
        ## Merge 1 - Order + Items para saber o valor do pedido
        df_completo = pd.merge(df_orders, df_items, on='order_id', how='inner')

        ## Merge 2 - Adicionando Costumer para saber quem é o cliente unico
        df_completo = pd.merge(df_completo, df_costumer, on="customer_id", how='inner')

        ## 4.0 Feature Engineering: Calculo de RFM

        ## Definição de dada da referencia
        ## Ultima compra registrada + 1
        data_referencia = df_completo['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
        print(f"Data de referência para cálculos: {data_referencia}")
        
        ## Agrupamento por cliente único
        df_rfm = (
            df_completo
            .groupby('customer_unique_id')
            .agg(
                {
                    'order_purchase_timestamp': lambda x: (data_referencia - x.max()).days,
                    'order_id': 'nunique',
                    'price': 'sum'
                }
            )
            .reset_index()
        )

        # Renomear colunas para facilitar
        df_rfm.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']

        # Filtrar outliers ou ruídos (opcional, mas bom para garantir consistência)
        # Ex: Clientes com valor monetário 0 (possíveis erros de sistema)
        df_rfm = df_rfm[df_rfm['monetary'] > 0]

        # 5. Salvar na pasta Processed com nome rfm_data.csv
        caminho_saida = os.path.join('data', 'processed', 'rfm_data.csv')
        # Garantir que a pasta existe
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        
        df_rfm.to_csv(caminho_saida, index=False)
        print(f"Arquivo salvo com sucesso em: {caminho_saida}")

        return df_rfm


    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        return None
    except pd.errors.EmptyDataError as e:
        print(f"Erro: Arquivo vazio ou inválido - {e}")
        return None
    except Exception as e:
        print(f"Erro desconhecido ao carregar dados: {e}")
        return None

    

    
    #df_orders = df_orders[df_orders['order_status'] == 'delivered'].copy()
    

if __name__ == "__main__":
    carregar_e_processar_dados()
