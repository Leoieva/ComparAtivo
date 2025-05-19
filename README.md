# ComparAtivo+

Utilizando o **Python** para calcular e exibir a rentabilidade, o risco e o desempenho de qualquer ação brasileira ou FII (Fundo Imobilíario de Investimento) onde é possível montar carteiras adequadas com boa performance.

A entrada de dados é como simular uma carteira, é preciso informar o nome de cada ativo, o período de tempo, o capital investido e o peso de cada investimento.

Na saída será gerado um arquivo .pdf _"relatorio_carteira.pdf"_ com os seguintes análises: Taxa de retorno de cada ativo e da carteira, Risco de cada ativo e carteira Resultado do peso, do valor aplicado em cada ativo, Correlação entre ativos, Gráfico da evolução do preço da ação / cota VS Índice Ibovespa.    
_Obs: A rentabilidade do ativo não utiliza o retorno mensal de dividendos apenas a valorização da cota._

**Exemplo prático**

Pesquisei ao acaso 2 ações de cada um dos 5 setores perenes do mercado financeiro brasileiro e configurei o input do programa:
_Obs:_
- _Setores: Banco, Energia, Saneamento, Materiais básicos e Saúde_
- _Pesos: valor igual para todos os 10 ativos_
- _Capital investido: R$ 10.000,00_

![image](https://github.com/user-attachments/assets/62dbbfa3-808a-4853-8598-b3d651134649)

E após a visualização do relatório em pdf gerado, de forma rápida e interativa, consegui tirar as seguintes conclusões sobre cada ativo:
- O setor mais arriscado é Saúde e menos arriscado é Banco.
- Os ativos com maior rentabilidade foram a Sabesp (Saneamento) com 24% ao ano e a Cemig (Energia) com quase 20% ao ano.
- Nenhum setor ou ação se correlacionam fortemente ao chegar no valor 1.0.
- Os setor Banco e Saneamento foram os mais rentáveis acima do Índice Ibovespa.
- A carteira apresenta risco muito baixo (menor que 50%), porém a sua média de retorno ficou em -0.84% devido a desvalorização significativa da Kablin, Hapvida e RD Saúde.

**O foco do projeto é deixar uma tomada de decisão financeira mais sólida.**
Logo, utilizando a análise acima, podemos usar a lógica de aplicar maior peso nos setores mais rentáveis.
Resultado: 
- O risco anual de 14% caiu para menos de 1%.
- Com apenas um período de 1 ano simulado, houve um lucro de R$ 908,00 pela valorização da cota.
- A perda foi apenas de R$ 150,00 comparada aos quase R$ 1.000,00 de prejuízo da simulação anterior.




