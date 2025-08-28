import re
import os
import pandas as pd
from tqdm import tqdm

PASTA_BASE = './CommentSentimentAPI/data/datasets/treinado'
PASTA_BASE_N = './CommentSentimentAPI/data/datasets/normal'
PASTA_TRATADA = './CommentSentimentAPI/data/datasets/tratado'

class TextAPI():
    @staticmethod
    def limpar_texto(texto: str) -> str:
        if not isinstance(texto, str):
            return "N/A"
        
        texto = texto.lower()
        
        texto = re.sub(r"http\\S+", "", texto)
        texto = re.sub(r"@[A-Za-z0-9_]+", "", texto)
        texto = re.sub(r"[^a-zà-ÿ# ]", "", texto)
        
        return texto

class DataAPI():
    def __init__(self):
        self.DATASETS = {}
        self.COLUNAS = {}
        self.CONFIG = {
            'coluna_texto': None,
            'coluna_emocao': None
        }
        self.emocoes_map_ml = {
            1: 'Neutro',
            2: 'Felicidade',
            3: 'Raiva',
            4: 'Surpresa',
            5: 'Tristeza',
            6: 'Disgosto',
            7: 'Medo'
        }
        self.emocoes_map_n = {
            0: 'Neutro',
            1: 'Felicidade',
            2: 'Raiva',
            3: 'Medo',
            4: 'Surpresa',
            5: 'Tristeza',
            6: 'Nojo',
            7: 'Confiança'
        }
    
    # Geral
    def get_datasets(self, pasta: str) -> list:
        try:
            datasets = {}
            
            arquivos = os.listdir(pasta)
            contador = 0
            for arquivo in arquivos:
                contador += 1
                datasets.update({contador: arquivo})
            
            self.DATASETS = datasets
            return datasets
        except Exception as e:
            print(f"Erro ao listar os datasets: {e}")
            
            return {}

    def get_dataset_path(self, pasta: str, dataset_id: int) -> str:
        if dataset_id in self.DATASETS:
            return os.path.join(pasta, self.DATASETS[dataset_id])
        else:
            print("ID do dataset inválido.")
            return ""
    
    def carregar_dataset(self, caminho: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(caminho)
            
            return df
        except Exception as e:
            print(f"Erro ao carregar o dataset: {e}")
            
            return pd.DataFrame()

    def salvar_dataset(self, df: pd.DataFrame, arquivo: str) -> None:
        caminho = PASTA_TRATADA + "/" + arquivo
        
        try:
            df.to_csv(caminho, index=False)
            
            print(f"Dataset salvo em: {caminho}")
        except Exception as e:
            print(f"Erro ao salvar o dataset: {e}")

    def reduzir_dataset(self, df: pd.DataFrame, random: bool, limite: int) -> pd.DataFrame:
        if limite > 0 and limite < len(df) + 1:
            if random:
                return df.sample(n=limite, random_state=42)
            else:
                return df.head(limite)
        else:
            print("Limite inválido ou maior que o tamanho do dataset.")
            return df
        
    def get_colunas_df(self, df: pd.DataFrame) -> dict:
        colunas = {}
        contador = 0
        
        for coluna in df.columns.tolist():
            contador += 1
            
            colunas.update({contador: coluna})
            
        self.COLUNAS = colunas
        return colunas
        
    def get_dados_coluna(self, df: pd.DataFrame, id: int) -> list:
        if id in self.COLUNAS:
            coluna = self.COLUNAS[id]
            
            return df[coluna].tolist()
        else:
            print("ID da coluna inválido.")
            
            return []
        
    def get_nome_coluna_id(self, id: int) -> str:
        if id in self.COLUNAS:
            coluna = self.COLUNAS[id]
            
            return coluna
        else:
            print("ID da coluna inválido.")
            
            return []

    def definir_coluna(self, tipo: int, id: int) -> None:
        if id in self.COLUNAS:
            coluna = self.COLUNAS[id]
            
            if tipo == 1:
                self.CONFIG['coluna_texto'] = coluna
            elif tipo == 2:
                self.CONFIG['coluna_emocao'] = coluna
            else:
                print("Tipo inválido. Use 1 para texto e 2 para emoção.")
        else:
            print("ID da coluna inválido.")

    # Datasets Treinados LLM's
    def tratar_coluna_emocoes(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.CONFIG['coluna_emocao'] is None:
            print("Coluna de emoção não definida.")
            return df

        coluna_emocao = self.CONFIG['coluna_emocao']

        tqdm.pandas(desc="Limpando emoções")
        df['emocoes_formatada'] = (
            df[coluna_emocao]
            .progress_apply(lambda x: re.sub(rf"^{coluna_emocao}: ?", "", str(x)))
            .apply(lambda x: re.sub(r'"', "", x))
            .apply(lambda x: int(x) if x.isdigit() else -1)
        )

        return df

    def tratar_coluna_texto(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.CONFIG['coluna_texto'] is None:
            print("Coluna de texto não definida.")
            return df

        coluna_texto = self.CONFIG['coluna_texto']

        tqdm.pandas(desc="Limpando textos")
        df['texto_formatado'] = (
            df[coluna_texto]
            .progress_apply(lambda x: re.sub(rf"^{coluna_texto}: ?", "", str(x)))
            .apply(lambda x: re.sub(r'"', "", x))
        )
        df['texto_limpo'] = df['texto_formatado'].progress_apply(TextAPI.limpar_texto)

        return df
    
    def mapear_emocoes(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'emocoes_formatada' not in df.columns:
            print("Coluna 'emocoes_formatada' não encontrada.")
            return df

        tqdm.pandas(desc="Mapeando emoções")
        df['emocao_nome'] = df['emocoes_formatada'].progress_apply(
            lambda x: self.emocoes_map.get(x, 'Desconhecido')
        )

        return df
        
    # Datasets Geral
    def mapear_emocoes_n(self, coluna: int, df: pd.DataFrame) -> pd.DataFrame:
        coluna = self.get_nome_coluna_id(coluna)
        
        if coluna not in df.columns:
            print(f"Coluna {coluna} não encontrada.")
            return df

        tqdm.pandas(desc="Mapeando emoções")
        df['emocao_formatada'] = df[coluna]
        df['emocao_nome'] = df[coluna].progress_apply(
            lambda x: self.emocoes_map_n.get(x, 'Desconhecido')
        )

        return df
    
    # Comandos Geral LLM's
    def tratar_dataset_llm(self) -> bool:
        datasets = self.get_datasets(PASTA_BASE)
        print("Datasets disponíveis:", datasets)

        numero = int(input("Digite o número do dataset que deseja carregar: "))
        caminho = self.get_dataset_path(PASTA_BASE, numero)
        df = self.carregar_dataset(caminho)

        print(self.get_colunas_df(df))

        coluna_texto = int(input("Digite o número da coluna que contém os textos: "))
        self.definir_coluna(1, coluna_texto)

        coluna_emocoes = int(input("Digite o número da coluna que contém as emoções: "))
        self.definir_coluna(2, coluna_emocoes)

        df = self.tratar_coluna_texto(df)
        df = self.tratar_coluna_emocoes(df)
        df = self.mapear_emocoes(df)

        arquivo = input('Digite o nome para salvar o arquivo: ')
        self.salvar_dataset(df, arquivo + ".csv")
        
        return True
    
    # Comandos Geral Normal
    def tratar_dataset_normal(self) -> bool:
        datasets = self.get_datasets(PASTA_BASE_N)
        print("Datasets disponíveis:", datasets)

        numero = int(input("Digite o número do dataset que deseja carregar: "))
        caminho = self.get_dataset_path(PASTA_BASE_N, numero)
        df = self.carregar_dataset(caminho)
        
        print(self.get_colunas_df(df))
        print(df.head(2))
        coluna_texto = int(input("Digite o número da coluna que contém os textos: "))
        self.definir_coluna(1, coluna_texto)

        coluna_emocoes = int(input("Digite o número da coluna que contém as emoções: "))
        self.definir_coluna(2, coluna_emocoes)
        
        df = self.tratar_coluna_emocoes(df)
        df = self.tratar_coluna_texto(df)
        df = self.mapear_emocoes_n(coluna_emocoes, df)

        arquivo = input('Digite o nome para salvar o arquivo: ')
        self.salvar_dataset(df, arquivo + ".csv")
    
if __name__ == '__main__':
    pass