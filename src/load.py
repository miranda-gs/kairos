import pandas as pd
import os

class ExcelLoader:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def load(self, df_categorias: pd.DataFrame, df_resumo: pd.DataFrame, filename: str = "relatorio_mensal.xlsx"):
        output_path = os.path.join(self.output_dir, filename)
        
        # Salvando em múltiplas abas usando o motor do openpyxl
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_resumo.to_excel(writer, sheet_name='Resumo Mensal', index=False)
            df_categorias.to_excel(writer, sheet_name='Gastos por Categoria', index=False)
        
        print(f"Relatório gerado com sucesso em: {output_path}")