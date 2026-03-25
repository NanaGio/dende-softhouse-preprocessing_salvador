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

        # Pega as colunas
        columns = self._get_target_columns(columns)
        # Pega a quantidade de linhas por coluna
        row_count = len(next(iter(self.dataset.values())))
        # Variável para Linhas selecionadas
        selected_rows = []

        # Verifica quais linhas tem algum dado com none
        for i in range(row_count):
            if any(self.dataset[col][i] is None for col in columns):
                selected_rows.append(i)
        # cria novo dataset vazio com base no dataset original
        result = {col: [] for col in self.dataset}

        # Adiciona os dados selecionados
        for i in selected_rows:
            for col in self.dataset:
                result[col].append(self.dataset[col][i])

        return result

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

        # Pega as colunas
        columns = self._get_target_columns(columns)
        # Pega a quantidade de linhas por coluna
        row_count = len(next(iter(self.dataset.values())))
        # Variável para Linhas selecionadas
        selected_rows = []

        # Verifica quais linhas não tem nenhum dado com none
        for i in range(row_count):
            if all(self.dataset[col][i] is not None for col in columns):
                selected_rows.append(i)

        # cria novo dataset vazio com base no dataset original
        result = {col: [] for col in self.dataset}

        # Adiciona os dados selecionados
        for i in selected_rows:
            for col in self.dataset:
                result[col].append(self.dataset[col][i])

        return result

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

        # pega as colunas
        columns = self._get_target_columns(columns)
        # Preenche valores Nones com value
        for col in columns:
            for i, v in enumerate(self.dataset[col]):
                if v is None:
                    self.dataset[col][i] = value

        return self.dataset

    def dropna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Remove as linhas que contêm valores nulos (None) nas colunas especificadas.
        Modifica o dataset da classe.

        Args:
            columns (Set[str]): Colunas a serem verificadas para valores nulos. Se vazio, todas as colunas são verificadas.
        """
        # Pega as colunas
        columns = self._get_target_columns(columns)
        # Pega a quantidade de linhas por coluna
        row_count = len(next(iter(self.dataset.values())))
        # cria variável que recebe os dados
        keep_rows = []
        # Verifica quais linhas não tem nenhum dado com none
        for i in range(row_count):
            if all(self.dataset[col][i] is not None for col in columns):
                keep_rows.append(i)
        # cria novo dataset vazio com base no dataset original
        new_dataset = {col: [] for col in self.dataset}
        # Adiciona os dados selecionados
        for i in keep_rows:
            for col in self.dataset:
                new_dataset[col].append(self.dataset[col][i])

        # altera o dataset original com os dados selecionados
        # CORREÇÃO: Modifica o conteúdo das listas originais (in-place) para refletir fora da classe
        for col in self.dataset:
            self.dataset[col][:] = new_dataset[col]

        return self.dataset


class Scaler:

    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        return list(columns) if columns else list(self.dataset.keys())

    # Função para retornar as colunas que o utilizador  escolher e retorna todas caso nenhuma seja escolhida

    def _is_number(self, value: Any) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    # Verificação de segurança para avaliar se o valor é realmente um numero, garantindo tambem que esse numero nao seja um booleano

    def minMax_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        # Define o que vai ser recebido e devolvido
        target_columns = self._get_target_columns(columns)
        # Chama a função get target para saber o que vai ser recebido de fato

        dataset_processado = copy.deepcopy(self.dataset)

        # Laço de repetição, passa por cada coluna e verifica se ela de fato existe nos dados
        for col in target_columns:
            if col in dataset_processado:
                # Cria uma lista temporarias so com numeros reais, ignorando textos e nones
                values = [v for v in dataset_processado[col] if self._is_number(v)]
                # Se a coluna so tiver texto, a lista VALUES fica vazia, e o codigo pula pra proxima coluna
                if not values:
                    continue

                    # Descobre o maior e menor número de cada coluna, e busca o denominador subtraindo o menor valor do maior
                min_val = min(values)
                max_val = max(values)
                denom = max_val - min_val

                # cria uma nova lista parar guardar os valores novos
                nova_lista = []
                # le a coluna original (definida como x ) linha a linha
                for x in dataset_processado[col]:
                    # Se X for realmente um número e não for 0, realiza a operação
                    # Caso seja 0, ele apenas vai guardar o valor 0.0 na lista
                    # Se não for um número real ou for um NONE apenas repete na lista sem alterações
                    if self._is_number(x):
                        if denom == 0:
                            nova_lista.append(0.0)
                        else:
                            nova_lista.append((x - min_val) / denom)
                    else:
                        nova_lista.append(x)

                dataset_processado[col] = nova_lista

        # retorna os dados atualizados quando as colunas acabarem
        return dataset_processado

    def standard_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        target_cols = self._get_target_columns(columns)

        for col in target_cols:
            if col in self.dataset:
                values = [v for v in self.dataset[col] if self._is_number(v)]
                if not values: continue

                mean_val = sum(values) / len(values)
                std_val = (sum((x - mean_val) ** 2 for x in values) / len(values)) ** 0.5

                # Atualiza a lista da coluna diretamente no self.dataset
                self.dataset[col] = [
                    ((x - mean_val) / std_val) if self._is_number(x) and std_val != 0 else x
                    for x in self.dataset[col]
                ]
        return self.dataset


class Encoder:
    """
    Aplica codificação em colunas categóricas.
    """

    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def label_encode(self, columns: Set[str]) -> Dict[str, List[Any]]:  # GIO
        """
        Converte cada categoria em uma coluna em um número inteiro.
        Modifica o dataset.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        values_modificados = {}

        for coluna in columns:
            values_modificado = self.dataset[coluna]
            # Aqui você gera a lista com "NULL"
            values_sem_nulo = ["NULL" if valor is None else valor for valor in values_modificado]

            # CORREÇÃO AQUI: Forçamos str() para que o sorted consiga comparar strings com strings
            valores_unicos = sorted(set(str(valor) for valor in values_sem_nulo))

            # Mapeamos o valor (string) para o índice
            valores_transformados = {valor: indice for indice, valor in enumerate(valores_unicos)}

            # Convertemos a coluna original usando o mapa
            coluna_convertida = [valores_transformados[str(valor)] for valor in values_sem_nulo]

            self.dataset[coluna] = coluna_convertida
            values_modificados[coluna] = coluna_convertida

        return values_modificados

    def oneHot_encode(self, columns: Set[str]) -> Dict[str, List[Any]]:  # GIO
        """
        Cria novas colunas binárias para cada categoria nas colunas especificadas (One-Hot Encoding).
        Modifica o dataset adicionando e removendo colunas.

        Args:
            columns (Set[str]): Colunas categóricas para codificar.
        """
        categorias = {}

        for coluna in columns:
            categorias_in_coluna = self.dataset[coluna]  # identificando as categorias na coluna
            categorias_sem_nulo = ["NULL" if valor is None else valor for valor in
                                   categorias_in_coluna]  # retirando os nulos
            categorias_unicas = set(categorias_sem_nulo)  # separando as únicas
            categorias[coluna] = categorias_unicas  # substituindo

            # criando a categoria especifica f"{x}_{x}"
            for categoria in categorias_unicas:
                nova_coluna = f"{coluna}_{categoria}"  #
                self.dataset[nova_coluna] = [0] * len(self.dataset[coluna])

                # preenchendo com 1, onde a categoria coincide
                for i in range(len(self.dataset[coluna])):
                    if categorias_sem_nulo[i] == categoria:
                        self.dataset[nova_coluna][i] = 1

            # deletando a coluna primaria
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

        # Pega o tamanho de cada coluna (lista) do dataset
        lengths = [len(col) for col in self.dataset.values()]

        # Se o dataset estiver vazio, não há o que validar
        if not lengths:
            return  # Dataset vazio é considerado válido

        # Define o tamanho esperado com base na primeira coluna
        first_length = lengths[0]

        # Verifica se todas as colunas possuem o mesmo tamanho
        for l in lengths:
            # Se encontrar uma coluna com tamanho diferente, lança erro
            if l != first_length:
                raise ValueError("Todas as colunas devem ter o mesmo número de linhas.")

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