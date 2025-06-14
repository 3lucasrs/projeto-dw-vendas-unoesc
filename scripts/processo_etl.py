import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

def carregar_dimensao(engine, df, nome_tabela, colunas_df, colunas_rename, chave_unica_df):
    print(f"\n--- Iniciando carga da Dimensão: {nome_tabela} ---")
    try:
        with engine.connect() as connection:
            for coluna in colunas_df:
                if df[coluna].dtype == 'object':
                    df[coluna] = df[coluna].str.strip()

            dim_source = df[colunas_df].drop_duplicates(subset=[chave_unica_df], keep='first')
            dim_source = dim_source.rename(columns=colunas_rename)

            result = connection.execute(text(f"SELECT {colunas_rename[chave_unica_df]} FROM {nome_tabela}"))
            existing_ids = [row[0] for row in result]
            print(f"Encontrados {len(existing_ids)} registros existentes no DW.")

            dim_new = dim_source[~dim_source[colunas_rename[chave_unica_df]].isin(existing_ids)]

            if not dim_new.empty:
                print(f"Encontrados {len(dim_new)} novos registros para inserir...")
                dim_new.to_sql(nome_tabela, connection, if_exists='append', index=False)
                connection.commit()
                print(f"{len(dim_new)} novos registros inseridos com sucesso!")
            else:
                print("Nenhum registro novo para inserir. Tabela já está atualizada.")
    except Exception as e:
        print(f"ERRO na carga da dimensão {nome_tabela}: {e}")

def carregar_fato_vendas(engine, df):
    print("\n--- Iniciando carga da Tabela de Fatos: fatovendas ---")
    try:
        with engine.connect() as connection:
            print("Limpando a tabela de fatos para uma carga completa...")
            connection.execute(text("TRUNCATE TABLE fatovendas RESTART IDENTITY;"))
            connection.commit()

            map_produto = pd.read_sql("SELECT id_produto, id_produto_original FROM dimproduto", connection)
            map_cliente = pd.read_sql("SELECT id_cliente, id_cliente_original FROM dimcliente", connection)
            map_local = pd.read_sql("SELECT id_local, id_local_original FROM dimlocal", connection)
            map_tempo = pd.read_sql("SELECT datacompleta FROM dimtempo", connection)
            map_tempo['datacompleta'] = pd.to_datetime(map_tempo['datacompleta'])
            
            df['product_id'] = df['product_id'].str.strip()
            df['customer_id'] = df['customer_id'].str.strip()
            df['local_id_original'] = df['city'].str.strip() + '_' + df['state'].str.strip()
            df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)

            fato_df = df.merge(map_produto, left_on='product_id', right_on='id_produto_original')
            fato_df = fato_df.merge(map_cliente, left_on='customer_id', right_on='id_cliente_original')
            fato_df = fato_df.merge(map_local, left_on='local_id_original', right_on='id_local_original')
            fato_df = fato_df.merge(map_tempo, left_on='order_date', right_on='datacompleta')

            fato_df_final = fato_df[['order_id', 'datacompleta', 'id_produto', 'id_cliente', 'id_local', 'sales']]
            fato_df_final = fato_df_final.rename(columns={
                'order_id': 'id_pedido_original',
                'datacompleta': 'id_data',
                'sales': 'valorvenda'
            })

            print(f"Preparando para inserir {len(fato_df_final)} registros na tabela de fatos...")
            fato_df_final.to_sql('fatovendas', connection, if_exists='append', index=False)
            connection.commit()
            print("Carga da tabela de fatos concluída com sucesso!")

    except Exception as e:
        print(f"ERRO na carga da tabela de fatos: {e}")

def main():
    db_user = 'postgres'
    db_password = 'root'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'dw_vendas'

    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        print("Conexão com o PostgreSQL bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return

    try:
        caminho_arquivo = Path(__file__).parent.parent / 'data' / 'superstore_sales.csv'
        df = pd.read_csv(caminho_arquivo, encoding='latin-1')
        print("Arquivo CSV carregado com sucesso.")

        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
        print("Colunas do DataFrame padronizadas.")
    except Exception as e:
        print(f"ERRO na extração/transformação: {e}")
        return

    carregar_dimensao(engine, df, 'dimproduto', ['product_id', 'product_name', 'category', 'sub_category'], 
                      {'product_id': 'id_produto_original', 'product_name': 'nomeproduto', 'category': 'categoria', 'sub_category': 'subcategoria'}, 'product_id')
    
    carregar_dimensao(engine, df, 'dimcliente', ['customer_id', 'customer_name', 'segment'], 
                      {'customer_id': 'id_cliente_original', 'customer_name': 'nomecliente', 'segment': 'segmento'}, 'customer_id')
    
    df['local_id_original'] = df['city'].str.strip() + '_' + df['state'].str.strip()
    carregar_dimensao(engine, df, 'dimlocal', ['local_id_original', 'city', 'state', 'country', 'region'],
                      {'local_id_original': 'id_local_original', 'city': 'cidade', 'state': 'estado', 'country': 'pais', 'region': 'regiao'}, 'local_id_original')
    
    df_tempo = pd.DataFrame({'datacompleta': pd.to_datetime(df['order_date'], dayfirst=True).unique()})
    df_tempo['ano'] = df_tempo['datacompleta'].dt.year
    df_tempo['mes'] = df_tempo['datacompleta'].dt.month
    df_tempo['dia'] = df_tempo['datacompleta'].dt.day
    df_tempo['trimestre'] = df_tempo['datacompleta'].dt.quarter
    carregar_dimensao(engine, df_tempo, 'dimtempo', ['datacompleta', 'ano', 'mes', 'dia', 'trimestre'],
                      {'datacompleta': 'datacompleta', 'ano': 'ano', 'mes': 'mes', 'dia': 'dia', 'trimestre': 'trimestre'}, 'datacompleta')

    carregar_fato_vendas(engine, df)

    print("\nProcesso de ETL concluído.")

if __name__ == "__main__":
    main()
