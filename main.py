from funcoes import *

''' AÇÕES BRASILEIRAS QUE MAIS PAGARAM DIVIDENDOS EM 12 MESES (05/2024 a 05/2025)
Bancos: 'itub4.sa', 'bbdc4.sa', 'bbas3.sa', 'sanb11.sa', 'abcb4.sa'
Energia: 'taee4.sa', 'isae4.sa', 'cple3.sa', 'cmig4.sa', 'egie3.sa'
Saneamento: 'sbsp3.sa', 'csmg3.sa', 'sapr11.sa'
Seguros: 'bbse3.sa', 'cxse3.sa', 'pssa3.sa'
Materiais básicos: 'vale3.sa', 'ggbr4.sa', 'suzb3.sa', 'klbn4.sa', 'csna3.sa'
Diversos: 'vivt3.sa', 'b3sa3.sa', 'mrfg3.sa', 'jbss3.sa', 'petr4.sa'
'''

inicio = data_inicio(2024, 4, 1)
fim = data_fim(2025, 4, 1)
ativos_indices = ['brco11.sa', 'hglg11.sa', 'xplg11.sa', 'vilg11.sa', 'rbrl11.sa', 'blmg11.sa']

# Distribuir o peso de cada ativo conforme sua escolha até somar em 1.0
# peso = []

# Distribuir o peso de cada ativo de forma igual
total_ativos_indices = 6
pesos = [1/total_ativos_indices] * total_ativos_indices

capital = 12000

df = historico_ativo(ativos_indices, inicio, fim)
df_e_ibov = historico_ativo(ativos_indices + ['^BVSP'], inicio, fim)

gerar_relatorio_pdf(df, df_e_ibov, pesos, capital, inicio, fim)