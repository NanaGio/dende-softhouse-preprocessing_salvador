from dende_statistics import Statistics
from typing import Dict, List, Set, Any

class MissingValueProcessor:
    """
    Processa valores ausentes (representados como None) no dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        """Retorna as colunas a serem processadas. Se 'columns' for vazio, retorna todas as colunas."""
        return list(columns) if columns else list(self.dataset.keys())

    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que possuem
        pelo menos um valor nulo (None) em uma das colunas especificadas.

        Args:
            columns (Set[str]): Um conjunto de nomes de colunas a serem verificadas.
                            Se vazio, todas as colunas são consideradas.

        Returns:
            Dict[str, List[Any]]: Um dicionário representando as linhas com valores nulos.
        """
        pass

    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que não possuem
        valores nulos (None) em nenhuma das colunas especificadas.

        Args:
            columns (Set[str]): Um conjunto de nomes de colunas a serem verificadas.
                               Se vazio, todas as colunas são consideradas.

        Returns:
            Dict[str, List[Any]]: Um dicionário representando as linhas sem valores nulos.
        """
        pass

    def fillna(self, columns: Set[str] = None, value: Any = 0) -> Dict[str, List[Any]]:
        """
        Preenche valores nulos (None) nas colunas especificadas com um valor fixo.
        Modifica o dataset da classe.

        Args:
            columns (Set[str]): Colunas onde o preenchimento será aplicado. 
                               Se vazio, aplica a todas as colunas do dataset.
            value (Any): Valor a ser inserido no lugar de None.

        Returns:
            Preprocessing: A própria instância (self) para permitir encadeamento.
        """
        pass

    def dropna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Remove as linhas que contêm valores nulos (None) nas colunas especificadas.
        Modifica o dataset da classe.

        Args:
            columns (Set[str]): Colunas a serem verificadas para valores nulos. Se vazio, todas as colunas são verificadas.
        """
        pass


class Scaler:
    """
    Aplica transformações de escala em colunas numéricas do dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        return list(columns) if columns else list(self.dataset.keys())

    def minMax_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Aplica a normalização Min-Max ($X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}$)
        nas colunas especificadas. Modifica o dataset.

        Args:
            columns (Set[str]): Colunas para aplicar o scaler. Se vazio, tenta aplicar a todas.
        """
        pass

    def standard_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Aplica a padronização Z-score ($X_{std} = \frac{X - \mu}{\sigma}$)
        nas colunas especificadas. Modifica o dataset.

        Args:
            columns (Set[str]): Colunas para aplicar o scaler. Se vazio, tenta aplicar a todas.
        """
        pass

class Encoder:
    """
    Aplica codificação em colunas categóricas.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def label_encode(self, columns: Set[str]) -> Dict[str, List[Any]]: # GIO
        """
        Converte cada categoria em uma coluna em um número inteiro.
        Modifica o dataset.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        values_modificados = {}

        for coluna in columns:
            values_modificado = self.dataset[coluna]#coletando a coluna
            values_sem_nulo = ["NULL" if valor is None else valor for valor in values_modificado]#substituindo valores nulos por null
            valores_unicos = sorted(set(values_sem_nulo))#colocando em ordem crescente, e separando por valores unicos
            valores_transformados = { valor: indice for indice,  valor in enumerate(valores_unicos)}#orgazinando os indices da coluna com enumerate
            coluna_convertida = [valores_transformados[valor] for valor in values_sem_nulo]#substituindo cada valor string por int
            self.dataset[coluna] = coluna_convertida#injetando a transformação na coluna novamente
            values_modificados[coluna] = coluna_convertida#transformação final com variável

        return values_modificados

    def oneHot_encode(self, columns: Set[str]) -> Dict[str, List[Any]]: #GIO
        """
        Cria novas colunas binárias para cada categoria nas colunas especificadas (One-Hot Encoding).
        Modifica o dataset adicionando e removendo colunas.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        categorias = {}

        for coluna in columns:
            categorias_in_coluna = self.dataset[coluna]#identificando as categorias na coluna
            categorias_sem_nulo = ["NULL" if valor is None else valor for valor in categorias_in_coluna]#retirando os nulos
            categorias_unicas = set(categorias_sem_nulo)#separando as únicas
            categorias[coluna] = categorias_unicas#substituindo

            #criando a categoria especifica f"{x}_{x}"
            for categoria in categorias_unicas:
                nova_coluna = f"{coluna}_{categoria}" #
                self.dataset[nova_coluna] = [0] * len(self.dataset[coluna])

                #preenchendo com 1, onde a categoria coincide
                for i in range(len(self.dataset[coluna])):
                    if categorias_sem_nulo[i] == categoria:
                        self.dataset[nova_coluna][i] = 1

            #deletando a coluna primaria
            del self.dataset[coluna]

        return categorias

class Preprocessing:
    """
    Classe principal que orquestra as operações de pré-processamento de dados.
    Nota: Todos os métodos retornam o dicionário de dados (dataset), 
    o que encerra a possibilidade de encadeamento de métodos da classe.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        self._validate_dataset_shape()
        
        self.statistics = Statistics(self.dataset)
        self.missing_values = MissingValueProcessor(self.dataset)
        self.scaler = Scaler(self.dataset)
        self.encoder = Encoder(self.dataset)

    def _validate_dataset_shape(self):
        """
        Valida se todas as listas (colunas) no dicionário do dataset
        têm o mesmo comprimento.
        """
        pass

    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.isna(). 
        Retorna um dicionário contendo apenas as linhas com valores nulos.
        """
        return self.missing_values.isna(columns)

    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.notna(). 
        Retorna um dicionário contendo apenas as linhas sem valores nulos.
        """
        return self.missing_values.notna(columns)

    def fillna(self, columns: Set[str] = None, value: Any = 0) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.fillna(). 
        Modifica e retorna o dicionário de dados com valores preenchidos.
        """
        return self.missing_values.fillna(columns, value)

    def dropna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.dropna(). 
        Modifica e retorna o dicionário de dados sem as linhas nulas.
        """
        return self.missing_values.dropna(columns)

    def scale(self, columns: Set[str] = None, method: str = 'minMax') -> Dict[str, List[Any]]:
        """
        Aplica escalonamento e retorna o dicionário de dados modificado.

        Args:
            columns (Set[str]): Colunas para aplicar o escalonamento.
            method (str): O método a ser usado: 'minMax' ou 'standard'.

        Returns:
            Dict[str, List[Any]]: O dataset com as colunas escalonadas.
        """
        if method == 'minMax':
            return self.scaler.minMax_scaler(columns)
        elif method == 'standard':
            return self.scaler.standard_scaler(columns)
        else:
            raise ValueError(f"Método de escalonamento '{method}' não suportado.")

    def encode(self, columns: Set[str], method: str = 'label') -> Dict[str, List[Any]]:
        """
        Aplica codificação e retorna o dicionário de dados modificado.

        Args:
            columns (Set[str]): Colunas para aplicar a codificação.
            method (str): O método a ser usado: 'label' ou 'oneHot'.
        
        Returns:
            Dict[str, List[Any]]: O dataset com as colunas codificadas.
        """
        if method == 'label':
            return self.encoder.label_encode(columns)
        elif method == 'oneHot':
            return self.encoder.oneHot_encode(columns)
        else:
            raise ValueError(f"Método de codificação '{method}' não suportado.")