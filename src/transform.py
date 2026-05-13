import pandas as pd

class FinanceTransformer:
    def process_data(self, df: pd.DataFrame, renda_mensal: float) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Processa os dados brutos e retorna o agrupamento por categoria e o resumo financeiro.
        """
        if df.empty:
            return df, pd.DataFrame()

        # Padronização de colunas (caso venham sujas)
        df.columns = df.columns.str.lower().str.strip()
        
        # Garantir que os valores são numéricos
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)

        # 1. Agrupar gastos por categoria
        gastos = df[df['tipo'].str.lower() == 'despesa']
        gastos_por_categoria = gastos.groupby('categoria', as_index=False)['valor'].sum()
        gastos_por_categoria = gastos_por_categoria.rename(columns={'valor': 'total_gasto'})
        gastos_por_categoria = gastos_por_categoria.sort_values(by='total_gasto', ascending=False)

        # 2. Calcular o balanço do mês
        total_despesas = gastos_por_categoria['total_gasto'].sum()
        total_receitas_extras = df[df['tipo'].str.lower() == 'receita']['valor'].sum()
        receita_total = renda_mensal + total_receitas_extras
        saldo_restante = receita_total - total_despesas

        resumo_mes = pd.DataFrame([{
            'Receita Total': receita_total,
            'Total Despesas': total_despesas,
            'Saldo Restante': saldo_restante
        }])

        return gastos_por_categoria, resumo_mes