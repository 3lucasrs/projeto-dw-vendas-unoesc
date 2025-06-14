import pandas as pd
from sqlalchemy import create_engine

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
        sql_query = """
        SELECT 
            f.valorvenda,
            p.categoria
        FROM 
            fatovendas f
        JOIN 
            dimproduto p ON f.id_produto = p.id_produto;
        """
        df_analise = pd.read_sql(sql_query, engine)
        print(f"Dados extraídos com sucesso! Total de {len(df_analise)} vendas para análise.")

        if df_analise.empty:
            print("Nenhum dado encontrado para análise. Execute o ETL primeiro.")
            return

        print("\n--- Análise de Vendas por Categoria ---")
        
        vendas_por_categoria = df_analise.groupby('categoria')['valorvenda'].sum().sort_values(ascending=False)
        
        vendas_por_categoria_formatado = vendas_por_categoria.map('R$ {:,.2f}'.format)
        
        print("Total de vendas por categoria:")
        print(vendas_por_categoria_formatado)
        
        print("\nAnálise concluída com sucesso!")

    except Exception as e:
        print(f"ERRO durante a análise dos dados: {e}")

if __name__ == "__main__":
    main()
