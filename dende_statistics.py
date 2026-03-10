class Statistics:
    """
    Uma classe para realizar cálculos estatísticos em um conjunto de dados.

    Atributos
    ----------
    dataset : dict[str, list]
        O conjunto de dados, estruturado como um dicionário onde as chaves
        são os nomes das colunas e os valores são listas com os dados.
    """

    def __init__(self, dataset):
        """
        Inicializa o objeto Statistics.

        Parâmetros
        ----------
        dataset : dict[str, list]
            O conjunto de dados, onde as chaves representam os nomes das
            colunas e os valores são as listas de dados correspondentes.
        """
        self.dataset = dataset

    def mean(self, column):
        """
        Calcula a média aritmética de uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            A média dos valores na coluna.
        """

        values = self.dataset[column]  # extraindo os dados da coluna

        if isinstance(values[0], str):  # validando dados
            print("Erro: coluna não numérica")
            return None

        if not values:  # caso a coluna esteja vazia
            return 0.0

        return sum(values) / len(values)  # calculando a média (soma dos valores dividido pela quantidade de valores)

    def median(self, column):
        """
        Calcula a mediana de uma coluna.

        A mediana é o valor central de um conjunto de dados ordenado.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            O valor da mediana da coluna.
        """

        values = sorted(self.dataset[column])  # extraindo os dados da coluna e ordenando
        n = len(values)  # quantidade de valores
        mid = n // 2  # índice do meio
        if all(isinstance(v, (int, float)) for v in values):  # validando dados
            if n % 2:
                return values[
                    mid]  # para dados numéricos, a mediana é a média dos dois valores centrais (se par) ou o valor do meio (se ímpar)
            else:
                return (values[mid - 1] + values[
                    mid]) / 2  # para dados numéricos, a mediana é a média dos dois valores centrais (se par) ou o valor do meio (se ímpar)
        else:
            return values[mid]  # para dados não numéricos, a mediana é o valor do meio (ou um dos dois do meio)

    def mode(self, column):
        """
        Encontra a moda (ou modas) de uma coluna.

        A moda é o valor que aparece com mais frequência no conjunto de dados.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        list
            Uma lista contendo o(s) valor(es) da moda.
        """
        values = self.dataset[column]  # extraindo os dados da coluna
        frequency = {}
        for value in values:  # contando a frequência de cada valor na coluna
            frequency[value] = frequency.get(value,
                                             0) + 1  # se o valor já existe no dicionário, incrementa a contagem; caso contrário, inicia a contagem em 1
        max_freq = max(frequency.values())  # encontrando a frequência máxima
        return [key for key, freq in frequency.items() if
                freq == max_freq]  # retornando uma lista com os valores que têm a frequência máxima (moda)

    def variance(self, column):
        """
        Calcula a variância populacional de uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            A variância dos valores na coluna.
        """
        if column not in self.dataset:
            return None

        dados = self.dataset[column]  # extraindo os dados das colunas

        if len(dados) == 0:  # caso a coluna esteja vazia
            return None

        media = sum(dados) / len(dados)  # tirando a média da coluna

        soma_quadrados = sum((x - media) ** 2 for x in dados)  # ao quadrado de cada desvio

        variancia_populacional = soma_quadrados / len(dados)  # média novamente

        return variancia_populacional

    def stdev(self, column):
        """
        Calcula o desvio padrão populacional de uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        float
            O desvio padrão dos valores na coluna.
        """
        variancia_populacional = self.variance(column)  # extraindo dados

        if variancia_populacional is None:  # caso a coluna esteja vazia
            return None

        desvio = variancia_populacional ** 0.5  # raiz quadrada

        return desvio

    def covariance(self, column_a, column_b):
        """
        Calcula a covariância entre duas colunas.

        Parâmetros
        ----------
        column_a : str
            O nome da primeira coluna (X).
        column_b : str
            O nome da segunda coluna (Y).

        Retorno
        -------
        float
            O valor da covariância entre as duas colunas.
        """
        valores_A = self.dataset[column_a]  # extraindo os dados das colunas
        valores_B = self.dataset[column_b]  # extraindo os dados das colunas

        n = len(valores_A)  # len para saber o tamanho
        media_A = sum(valores_A) / len(valores_A)  # média
        media_B = sum(valores_B) / len(valores_B)  # média

        desvios_A = []  # armazenar os devios da coluna A
        for x in valores_A:  # listando os desvios
            desvios_A.append(x - media_A)

        desvios_B = []  # armazenar os devios da coluna B
        for x in valores_B:  # listando os desvios
            desvios_B.append(x - media_B)

        soma_produtos = 0  # começand do zero a soma dos produtos

        for da, db in zip(desvios_A, desvios_B):  # zip para unir em pares
            soma_produtos += (da * db)  # armazenando a soma dos produtos

        resultado = soma_produtos / n  # média de relacionamento

        return float(resultado)

    def itemset(self, column):
        """
        Retorna o conjunto de itens únicos em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        set
            Um conjunto com os valores únicos da coluna.
        """
        valores_unicos = set(self.dataset[column])  # set -> separa os valores únicos

        return valores_unicos

    def absolute_frequency(self, column):
        """
        Calcula a frequência absoluta de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas contagens (frequência absoluta).
        """
        dados = self.dataset[column]

        frequencia = {}  # espaço para os valores

        for item in dados:
            if item in frequencia:  # aqui ele pergunta se esse item ja existe no dicionario
                frequencia[item] += 1  # se existir, ele vai somar +1 a esse item ja existente
            else:
                frequencia[item] = 1  # caso não exista, ele cria uma entrada nova e seta o valor como 1

        return frequencia

    def relative_frequency(self, column):
        """
        Calcula a frequência relativa de cada item em uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os itens e os valores são
            suas proporções (frequência relativa).
        """
        frequencia_absoluta = self.absolute_frequency(column)  # chama a função criada acima para fazer a contagem
        total = len(self.dataset[column])  # puxa o valor total de itens
        frequencia_relativa = {}  # espaço para as porcentagens

        for chave, contagem in frequencia_absoluta.items():  # separa as informações de frequencia absoluta em 2 campos
            frequencia_relativa[
                chave] = contagem / total  # faz com que o valor de frequencia relativa seja o resultado da divisão

        return frequencia_relativa

    def cumulative_frequency(self, column, frequency_method='absolute'):
        """
        Calcula a frequência acumulada (absoluta ou relativa) de uma coluna.

        A frequência é calculada sobre os itens ordenados.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        frequency_method : str, opcional
            O método a ser usado: 'absolute' para contagem acumulada ou
            'relative' para proporção acumulada (padrão é 'absolute').

        Retorno
        -------
        dict
            Um dicionário ordenado com os itens como chaves e suas
            frequências acumuladas como valores.
        """
        if frequency_method == 'absolute':
            dados = self.absolute_frequency(column)  # chama a função que conta, caso tenha sido solicitada
        else:
            dados = self.relative_frequency(column)  # se não, chama a função de porcentagem

        if column == 'priority':
            ordem = ['baixa', 'media', 'alta']  # força uma ordem especifica caso a coluna trabalhada seja prioridade
        else:
            ordem = sorted(dados.keys())  # do contrario a ordem é alfabética

        acumulado = 0  # valor inicial setado em 0
        resultado = {}  # campo vazio, preenchido pós soma

        for chave in ordem:
            valor_atual = dados.get(chave,
                                    0)  # pega o valor relativo a cada idem na fila, seta 0 caso n exista nenhum representante

            acumulado = acumulado + valor_atual  # soma
            resultado[chave] = acumulado  # preenche o campo resultado com o valor da soma

        return resultado

    def conditional_probability(self, column, value1, value2):
        """
        Calcula a probabilidade condicional P(X_i = value1 | X_{i-1} = value2).

        Este método trata a coluna como uma sequência e calcula a probabilidade
        de encontrar `value1` imediatamente após `value2`.

        Fórmula: P(A|B) = Contagem de sequências (B, A) / Contagem total de B

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        value1 : any
            O valor do evento consequente (A).
        value2 : any
            O valor do evento condicionante (B).

        Retorno
        -------
        float
            A probabilidade condicional, um valor entre 0 e 1.
        """
        # Recebe os valores do dataset
        values = self.dataset[column]

        # Contadores para a fórmula
        total_b = 0  # Quantas vezes o valor condicionante aparece (divisor)
        sucessos_ba = 0  # Quantas vezes a sequência (B -> A) ocorre (numerador)

        # Percorre até o penúltimo elemento
        for i in range(len(values) - 1):
            # Verifica se o elemento atual é o condicionante (B)
            if values[i] == value2:
                total_b += 1

                # Verifica se o consequente (A) aparece imediatamente após o condicionante (B)
                if values[i + 1] == value1:
                    sucessos_ba += 1
        # Proteção contra divisão por zero (caso value2 não exista ou seja o último)
        if total_b == 0:
            return 0.0

        return sucessos_ba / total_b

    def quartiles(self, column):
        """
        Calcula os quartis (Q1, Q2 e Q3) de uma coluna.

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).

        Retorno
        -------
        dict
            Um dicionário com os quartis Q1, Q2 (mediana) e Q3.
        """

        # Recebendo os valores do dataset
        values = sorted(self.dataset[column])
        n = len(values)

        # Caso a quantidade de valores for igual a zero
        if n == 0:
            return {"Q1": 0, "Q2": 0, "Q3": 0}

        # Cálculo do Q2 (Mediana)
        mid = n // 2
        if n % 2 == 0:
            q2 = (values[mid - 1] + values[mid]) / 2
            # O fatiamento começa do início até o mid
            lower_half = values[:mid]
            # O fatiamento começa do mid até o final
            upper_half = values[mid:]
        else:
            q2 = values[mid]
            # Para n ímpar, a mediana (Q2) é excluída de ambas as metades
            lower_half = values[:mid]
            upper_half = values[mid + 1:]

        # Cálculo do Q1 (Mediana da Metade Inferior)
        n_lower = len(lower_half)
        mid_l = n_lower // 2
        if n_lower % 2 == 0:
            q1 = (lower_half[mid_l - 1] + lower_half[mid_l]) / 2
        else:
            q1 = (lower_half[mid_l])

        # Cálculo do Q3 (Mediana da Metade Superior
        n_upper = len(upper_half)
        mid_u = n_upper // 2
        if n_upper % 2 == 0:
            q3 = (upper_half[mid_u - 1] + upper_half[mid_u]) / 2
        else:
            q3 = (upper_half[mid_u])

        return {"Q1": q1, "Q2": q2, "Q3": q3}

    def histogram(self, column, bins):
        """
        Gera um histograma baseado em buckets (intervalos).

        Parâmetros
        ----------
        column : str
            O nome da coluna (chave do dicionário do dataset).
        bins : int
            Número de buckets (intervalos).

        Retorno
        -------
        dict
            Um dicionário onde as chaves são os intervalos (tuplas)
            e os valores são as contagens.
        """

        valores = self.dataset[column]
        menor_valor, valor_maior = min(valores), max(valores)
        numero_bins = 4
        tamanho_bin = (valor_maior - menor_valor) / numero_bins

        # Criação os limites dos intervalos (os buckets)
        limites = []
        for i in range(numero_bins + 1):
            ponto = menor_valor + (i * tamanho_bin)
            limites.append(ponto)

        # Geração do dicionário com tuplas como chaves (Início, Fim)
        # Ex: {(20.0, 35.0): 0, (35.0, 50.0): 0, ...}
        histograma = {}
        for i in range(numero_bins):
            intervalo = (limites[i], limites[i + 1])
            histograma[intervalo] = 0

        # Realização da contagem
        for valor in valores:
            indice = int((valor - menor_valor) / tamanho_bin)

            # Ajuste para o valor máximo
            if indice == numero_bins:
                indice -= 1

            # Recupera a chave (tupla) correspondente ao índice para incrementar (Ex: (20.0, 35.0))
            chave_intervalo = (limites[indice], limites[indice + 1])
            histograma[chave_intervalo] += 1

        return histograma