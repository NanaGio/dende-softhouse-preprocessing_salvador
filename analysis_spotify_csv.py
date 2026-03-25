import csv

from dende_preprocessing import Preprocessing


def carregar_dataset_spotify(caminho_arquivo):
    """Lê o CSV e converte para dicionário de listas"""
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            colunas = leitor.fieldnames
            dataset = {coluna: [] for coluna in colunas}
            for linha in leitor:
                for coluna in colunas:
                    valor = linha[coluna].strip()
                    try:
                        # Converte para float se possível, senão None ou String
                        dataset[coluna].append(float(valor)) if valor != '' else dataset[coluna].append(None)
                    except ValueError:
                        dataset[coluna].append(valor if valor != '' else None)
            return dataset
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    # Recebendo os dados do Spotify
    dados_spotify = carregar_dataset_spotify("spotify_data clean.csv")

    if dados_spotify:
        # Instanciando o Preprocessing
        pipeline = Preprocessing(dados_spotify)

        # --- PROCESSAMENTO DE DADOS AUSENTES ---
        print("\n[1/3] Tratando nulos e integridade...")
        # Imputação: Preenche popularidade e seguidores com 0.0 se estiverem nulos [cite: 72]
        pipeline.fillna(columns={'track_popularity', 'artist_followers'}, value=0.0)
        # Remoção: Remove músicas sem nome ou artista para garantir a qualidade [cite: 66]
        pipeline.dropna(columns={'track_name', 'artist_name'})

        # --- TRANSFORMADORES DE ESCALA ---
        print("[2/3] Escalonando dados numéricos...")
        # Normalização Min-Max: Coloca seguidores e duração entre 0 e 1 [cite: 75]
        pipeline.scale(columns={'artist_followers', 'track_duration_min'}, method='minMax')
        # Padronização (Standard): Ajusta popularidade para Média 0 e Desvio 1 [cite: 76]
        pipeline.scale(columns={'track_popularity', 'artist_popularity'}, method='standard')

        # --- CODIFICADORES CATEGÓRICOS ---
        print("[3/3] Codificando categorias...")
        # One-Hot Encoding: Transforma tipo de álbum em colunas binárias (0 ou 1) [cite: 79]
        pipeline.encode(columns={'album_type'}, method='oneHot')
        # Label Encoding: Converte gêneros musicais em identificadores inteiros [cite: 79]
        pipeline.encode(columns={'artist_genres'}, method='label')

        # --- RESULTADO FINAL ---
        print("\n--- AMOSTRA DO DATASET PROCESSADO ---")

        # Supondo que as chaves sejam 'track_artist' e 'track_popularity'
        artista = dados_spotify["artist_name"]
        musica = dados_spotify['track_name']
        popularidade = dados_spotify['track_popularity']

        print("\n" + "=" * 68)
        print(f"| {'ARTISTA':23} | {'MÚSICA':<25} | {'POPULARIDADE':<12}")
        print("-" * 68)

        # Exibindo as 100 primeiras linhas para conferência
        for i in range(100):
            artist_name = artista[i]
            track_name = musica[i] if musica[i] is not None else "Desconhecido"
            popularity = popularidade[i]

            # Formatação para alinhar as colunas: <25 reserva 25 espaços à esquerda
            if isinstance(popularity, float):
                print(f"{artist_name[:25]:<25} | {track_name[:25]:<25} | {popularity:>12.4f}")
            else:
                print(f"{artist_name[:25]:<25} | {track_name[:25]:<25} | {popularity:>12}")

        print("=" * 68)