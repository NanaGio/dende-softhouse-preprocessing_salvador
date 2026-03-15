from dende_statistics import Statistics
from typing import Dict, List, Set, Any
import copy

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
    
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        
    def _get_target_columns (self, columns: Set[str]) -> List[str]:
        return list(columns) if columns else list(self.dataset.keys())
    #Função para retornar as colunas que o utilizador  escolher e retorna todas caso nenhuma seja escolhida
    
    def _is_number(self, value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    #Verificação de segurança para avaliar se o valor é realmente um numero, garantindo tambem que esse numero nao seja um booleano 
    
    def minMax_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        #Define o que vai ser recebido e devolvido 
        target_columns = self._get_target_columns(columns)  
        #Chama a função get target para saber o que vai ser recebido de fato

        dataset_processado = copy.deepcopy(self.dataset)
    
        #Laço de repetição, passa por cada coluna e verifica se ela de fato existe nos dados
        for col in target_columns:
            if col in dataset_processado:
                #Cria uma lista temporarias so com numeros reais, ignorando textos e nones 
                values = [v for v in dataset_processado[col] if self._is_number(v)]
                #Se a coluna so tiver texto, a lista VALUES fica vazia, e o codigo pula pra proxima coluna 
                if not values:
                    continue 
                
                #Descobre o maior e menor número de cada coluna, e busca o denominador subtraindo o menor valor do maior
                min_val = min(values)
                max_val = max(values)
                denom = max_val - min_val

                #cria uma nova lista parar guardar os valores novos
                nova_lista = []
                #le a coluna original (definida como x ) linha a linha 
                for x in dataset_processado[col]:
                    #Se X for realmente um número e não for 0, realiza a operação
                    #Caso seja 0, ele apenas vai guardar o valor 0.0 na lista
                    #Se não for um número real ou for um NONE apenas repete na lista sem alterações 
                    if self._is_number(x):
                        if denom == 0:
                            nova_lista.append(0.0)
                        else: 
                            nova_lista.append((x - min_val) / denom)
                    else:
                        nova_lista.append(x)
                        
                dataset_processado[col] = nova_lista
                
        #retorna os dados atualizados quando as colunas acabarem
        return dataset_processado
    
            
    def standard_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        target_cols = self._get_target_columns(columns)
        #mais uma vez busca as colunas que vao ser usadas 

        dataset_processado = copy.deepcopy(self.dataset)

        #olha pra cada coluna, mais uma vez filtrando numeros  e saltando para proxima coluna se não houver
        for col in target_cols:
            if col in dataset_processado:
                values = [v for v in dataset_processado[col] if self._is_number(v)]
                if not values: 
                    continue 

                #faz o calculo do desvio padrão
                n = len(values) #len busca o número de valores existentes
                mean_val = sum(values) / n #soma todos e divide pela quantidade de valores
                #calculo de variancia, pega cada número, tira a média e eleva ao quadrado 
                soma_quadrados = sum((x - mean_val) ** 2 for x in values)
                #depois eleva a 0.5 para buscar a raiz quadrada da variância(que é o desvio padrão)
                std_val = (soma_quadrados / n) ** 0.5

                #cria nova lista 
                nova_lista = []
                #mais uma vez passando linha por linha na coluna original
                for x in dataset_processado[col]:
                    if self._is_number(x):
                        #verifica mais uma vez se é número e se não é 0
                        if std_val == 0:
                            nova_lista.append(0.0)
                        else: 
                            #Fórmula = (valor-media)/desvio_padrao
                            nova_lista.append((x - mean_val) / std_val)
                    else: 
                        #Mantém textos e NONES sem alteração 
                        nova_lista.append(x)

                #Atualiza a coluna no dicionário    
                dataset_processado[col] = nova_lista
        #retorna a lista pronta 
        return dataset_processado
   

class Encoder:
    """
    Aplica codificação em colunas categóricas.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def label_encode(self, columns: Set[str]) -> Dict[str, List[Any]]:
        """
        Converte cada categoria em uma coluna em um número inteiro.
        Modifica o dataset.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        pass

    def oneHot_encode(self, columns: Set[str]) -> Dict[str, List[Any]]:
        """
        Cria novas colunas binárias para cada categoria nas colunas especificadas (One-Hot Encoding).
        Modifica o dataset adicionando e removendo colunas.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        pass


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