
# 🌴 Dende Preprocessing

O **Dende Preprocessing** é a biblioteca oficial de tratamento de dados da Dende Softhouse, desenvolvida especificamente para o ecossistema de gestão de eventos da empresa.

Seu objetivo é transformar dados brutos e ruidosos em *datasets* estruturados e prontos para alimentar modelos de recomendação e soluções de inteligência de negócio.

---

## 🏗️ Integridade e Estrutura dos Dados

Antes de qualquer processo de normalização ou codificação, é essencial garantir que o dataset esteja consistente e livre de problemas estruturais. Dados incompletos ou inconsistentes podem comprometer análises estatísticas, gerar resultados incorretos em modelos de recomendação e reduzir a confiabilidade das informações.

No projeto Dende Preprocessing, os dados são representados utilizando a estrutura `Dict[str, List]`.

* **Chaves (`str`):** Representam as colunas do dataset.
* **Listas (`List`):** Representam os valores daquela coluna.

Cada posição dentro das listas corresponde a uma linha do conjunto de dados. Por exemplo, se um dataset possui três colunas, cada lista terá valores na mesma posição representando a mesma linha de informação. Essa estrutura permite manipular os dados de forma simples, mas também exige cuidados rigorosos para garantir que todas as listas tenham o mesmo tamanho e que os dados estejam alinhados e consistentes.

---

## 🎯 Por que o Preprocessing é vital?

No contexto de eventos, lidamos frequentemente com dados imperfeitos e complexos. Caso esses problemas não sejam tratados adequadamente, eles podem causar distorções graves nas análises. Este módulo resolve três desafios críticos:

### 1️⃣ Valores Ausentes e Inconsistentes

Garante que falhas na coleta de dados (registros em branco ou nulos) não quebrem o funcionamento dos algoritmos de recomendação ou distorçam análises de negócio.

### 2️⃣ Viés de Escala

Evita que valores numericamente maiores (ex: ingresso a R$ 500) dominem variáveis menores (ex: 4.5 estrelas de avaliação) apenas por sua magnitude, colocando-os em uma mesma grandeza.

### 3️⃣ Conversão Categórica

Transforma dados textuais complexos (ex: "VIP", "Pista", "Show") em vetores numéricos que modelos matemáticos conseguem processar e interpretar adequadamente.

---

## 🚀 Principais Funcionalidades

| Módulo                | Descrição                                 | Principais Métodos                         |
| ---------------------- | ------------------------------------------- | ------------------------------------------- |
| **MissingValue** | Identificação e tratamento de dados nulos | `fillna`, `dropna`, `isna`, `notna` |
| **Scaler**       | Normalização e padronização de escalas  | `minMax_scaler`, `standard_scaler`      |
| **Encoder**      | Conversão de dados categóricos            | `label_encode`, `oneHot_encode`         |

### 🧹 Foco em Tratamento de Valores Ausentes

Valores ausentes são representados no dataset utilizando o valor `None`, indicando que determinada informação não está disponível. O módulo de tratamento de dados possui métodos específicos para manipular esses cenários:

* **`isna`**: Identifica a presença de valores ausentes. Retorna uma estrutura indicando, para cada posição, se existe ou não um valor nulo.
* **`notna`**: Realiza a operação inversa, indicando exatamente quais posições possuem valores válidos.
* **`dropna`**: Remove linhas inteiras que possuem valores ausentes em determinadas colunas. Ideal para quando registros incompletos comprometem a análise e não há um valor adequado para substituição.
* **`fillna`**: Substitui valores ausentes por um valor constante definido pelo usuário. Estratégia perfeita para manter todas as linhas do dataset, evitando a perda de dados durante a limpeza.

O tratamento adequado destas lacunas é a etapa fundamental que garante que o dataset final esteja robusto para as etapas posteriores de modelagem.

---

## 💻 Exemplo Prático: Pipeline de Eventos

Imagine preparar os dados de um evento para o sistema de recomendação:

```python
from dende_preprocessing import Preprocessing

# 1️⃣ Dados extraídos da base de eventos (Estrutura Dict[str, List])
raw_data = {
    "preco_ingresso": [150.0, 80.0, None, 300.0],
    "avaliacao": [4.8, None, 3.5, 5.0],
    "categoria": ["Show", "Teatro", "Show", "Workshop"]
}

# 2️⃣ Inicializando o motor de processamento
pipeline = Preprocessing(raw_data)

# 3️⃣ Tratando lacunas: Avaliações vazias tornam-se 0 (fillna)
pipeline.fillna(columns={"avaliacao"}, value=0)

# 4️⃣ Normalização: Coloca preços e avaliações na mesma grandeza (0 a 1)
pipeline.scale(columns={"preco_ingresso", "avaliacao"}, method='minMax')

# 5️⃣ Encoding: Transforma categorias em colunas binárias
dataset_final = pipeline.encode(columns={"categoria"}, method='oneHot')

print(dataset_final)
```
