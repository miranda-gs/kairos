import os
import pandas as pd
from src.extract import ExtractorFactory
from src.transform import FinanceTransformer
from src.load import ExcelLoader

def run_pipeline():
    raw_dir = 'data/raw'
    processed_dir = 'data/processed'
    RENDA_MENSAL_FIXA = 5000.00 # Exemplo de configuração de entrada
    
    all_dataframes = []

    print("Iniciando a extração dos arquivos...")
    # Iterar sobre todos os arquivos na pasta de dados brutos
    for filename in os.listdir(raw_dir):
        file_path = os.path.join(raw_dir, filename)
        
        if os.path.isfile(file_path):
            try:
                extractor = ExtractorFactory.get_extractor(file_path)
                df = extractor.extract(file_path)
                
                if not df.empty:
                    # Adiciona uma coluna rastreando a origem do dado (boa prática de linhagem de dados)
                    df['fonte_arquivo'] = filename
                    all_dataframes.append(df)
                    print(f"Extraído com sucesso: {filename}")
                else:
                    print(f"Arquivo vazio ou sem dados tabulares reconhecidos: {filename}")
                    
            except ValueError as e:
                print(f"Ignorando arquivo {filename}: {e}")
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")

    if not all_dataframes:
        print("Nenhum dado encontrado para processamento.")
        return

    # Consolidar todos os dados extraídos
    df_consolidado = pd.concat(all_dataframes, ignore_index=True)

    print("Iniciando a transformação dos dados...")
    transformer = FinanceTransformer()
    df_categorias, df_resumo = transformer.process_data(df_consolidado, renda_mensal=RENDA_MENSAL_FIXA)

    print("Carregando resultados...")
    loader = ExcelLoader(output_dir=processed_dir)
    loader.load(df_categorias, df_resumo)

    print("Pipeline ETL finalizada com sucesso.")

if __name__ == "__main__":
    run_pipeline()