import pandas as pd
import pdfplumber
import os
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> pd.DataFrame:
        pass

class CSVExtractor(BaseExtractor):
    def extract(self, file_path: str) -> pd.DataFrame:
        # Assumindo que o CSV tem colunas: 'data', 'descricao', 'categoria', 'valor', 'tipo' (receita/despesa)
        return pd.read_csv(file_path)

class PDFExtractor(BaseExtractor):
    def extract(self, file_path: str) -> pd.DataFrame:
        # A extração de PDF depende muito do layout. 
        # Este é um exemplo extraindo a primeira tabela encontrada.
        extracted_data = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    extracted_data.extend(table)
        
        if extracted_data:
            # Assumindo que a primeira linha seja o cabeçalho
            df = pd.DataFrame(extracted_data[1:], columns=extracted_data[0])
            # Conversão básica de tipos
            df['valor'] = df['valor'].replace(r'[\R$,]', '', regex=True).astype(float)
            return df
        return pd.DataFrame()

class ExtractorFactory:
    @staticmethod
    def get_extractor(file_path: str) -> BaseExtractor:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            return CSVExtractor()
        elif ext == '.pdf':
            return PDFExtractor()
        else:
            raise ValueError(f"Formato não suportado: {ext}")