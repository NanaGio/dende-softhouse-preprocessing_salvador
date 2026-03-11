import unittest
# Supondo que seu código esteja em um arquivo chamado preprocessing.py
# from preprocessing import MissingValueProcessor 
from dende_preprocessing import MissingValueProcessor



class TestMissingValueProcessor(unittest.TestCase):

    def setUp(self):
        """Prepara um dataset padrão antes de cada teste."""
        self.dataset = {
            'id': [1, 2, 3, 4, 5],
            'nome': ['Ana', 'Bia', None, 'Duda', 'Ema'],
            'nota': [10.0, None, 8.5, None, 7.0],
            'faltas': [1, 0, 2, 1, None]
        }
        self.processor = MissingValueProcessor(self.dataset)

    def test_isna_all_columns(self):
        """Testa isna sem especificar colunas (deve olhar todas)."""
        # Linhas com pelo menos um None: 1 (nota), 2 (nome), 3 (nota), 4 (faltas)
        resultado = self.processor.isna()
        
        # Apenas a linha 0 (Ana) está completa. O resultado deve ter 4 linhas.
        self.assertEqual(len(resultado['id']), 4)
        self.assertNotIn(1, resultado['id']) # ID 1 (Ana) não deve estar no isna
        self.assertIn(2, resultado['id'])    # ID 2 tem nota None

    def test_isna_specific_column(self):
        """Testa isna apenas para a coluna 'nota'."""
        resultado = self.processor.isna(columns={'nota'})
        
        # IDs com nota nula: 2 e 4
        self.assertEqual(len(resultado['id']), 2)
        self.assertCountEqual(resultado['id'], [2, 4])

    def test_notna_all_columns(self):
        """Testa notna (linhas sem nenhum nulo)."""
        resultado = self.processor.notna()
        
        # Apenas ID 1 não tem nenhum None
        self.assertEqual(len(resultado['id']), 1)
        self.assertEqual(resultado['id'][0], 1)

    def test_fillna_fixed_value(self):
        """Testa o preenchimento de Nones com um valor fixo."""
        # Preencher 'nota' com 0.0
        self.processor.fillna(columns={'nota'}, value=0.0)
        
        # Verifica se não existem mais Nones na coluna nota
        self.assertNotIn(None, self.dataset['nota'])
        self.assertEqual(self.dataset['nota'][1], 0.0)
        self.assertEqual(self.dataset['nota'][3], 0.0)
        # Verifica se a coluna 'nome' ainda tem None (não foi especificada)
        self.assertIn(None, self.dataset['nome'])

    def test_dropna_specific_column(self):
        """Testa a remoção de linhas baseada em colunas específicas."""
        # Remover linhas onde 'nome' é None (ID 3)
        self.processor.dropna(columns={'nome'})
        
        self.assertEqual(len(self.dataset['id']), 4)
        self.assertNotIn(3, self.dataset['id'])

    def test_dropna_all_columns(self):
        """Testa a remoção de linhas se houver qualquer nulo no dataset."""
        self.processor.dropna() # Sem colunas = todas
        
        # Sobra apenas o ID 1
        self.assertEqual(len(self.dataset['id']), 1)
        self.assertEqual(self.dataset['id'][0], 1)

    def test_logic_consistency(self):
        """Verifica se isna + notna resulta no tamanho original do dataset."""
        total_original = len(self.dataset['id'])
        qtd_isna = len(self.processor.isna()['id'])
        qtd_notna = len(self.processor.notna()['id'])
        
        self.assertEqual(qtd_isna + qtd_notna, total_original)

if __name__ == '__main__':
    unittest.main()