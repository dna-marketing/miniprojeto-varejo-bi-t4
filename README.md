# Miniprojeto Base Varejo - Kaggle

Projeto avaliativo do curso de Visualização de Dados e BI - T4 SENAI/SC
Aluna: Edna Amâncio Correia

Peguei a base Varejo do Kaggle e fiz uma análise exploratória com Python e pandas. Primeiro vi como a base era, depois achei os problemas, limpei, calculei as estatísticas do número de filhos dos clientes e fiz 2 agrupamentos (por gênero e por categoria).

Arquivos na pasta:
- Miniprojeto_EdnaACorreia_T4.py - o código
- miniprojeto_varejo.ipynb - o mesmo código no notebook
- Base Varejo.csv - base original
- df_limpo.csv - base depois da limpeza

## ETL e qualidade dos dados
ETL é Extrair, Transformar e Carregar. No meu projeto eu extraí a base do Kaggle, transformei limpando os problemas e carreguei salvando a base limpa num arquivo novo.

Aprendi que sem limpar a base os resultados saem errados. Essa base tinha colunas vazias, quase 100 mil linhas repetidas, categorias com #N/D e a data como texto. Se eu não tivesse tirado as repetidas por exemplo, todas as contagens iam ficar maiores do que são de verdade.



## Conclusoes
1. A base tinha muitas linhas duplicadas (96.553), que teriam inflado o resultado das contagens. Depois da limpeza ficaram 733.447 itens.

2. Optei por manter as categorias #N/D para não perder histórico de vendas e só renomeei como "Sem Categoria". Se apagasse, perderia 3.650 vendas. Assim os dados ficam e o problema continua visível.

3. Cada compra tem, em média, 40 itens (733.447 / 18.471 = 40), parecendo compras de supermercado, tipo compra do mês.

4. Olhando os 1000 clientes, a maioria não tem filhos (a mediana e a moda deram 0). A média deu 1 filho por cliente, mas fica um pouco mais alta porque alguns clientes têm 3 ou 4 filhos.

5. As mulheres compram mais, cerca de 31 mil itens a mais. Ranking das categorias: Alimentos, Higiene, Limpeza, Bebidas, Pet e Acessórios. Alimentos sozinho é mais da metade das vendas o que é natural nesse perfil de varejo. Porém, o perfil de compra entre os gêneros não tem nenhuma discrepância.

6. Problemas que ainda ficam na base: não tem coluna de valor (R$), então só deu para analisar Não tem valor em R$: você sabe quantos itens foram vendidos, mas não quanto dinheiro entrou. Não dá para saber, por exemplo, qual categoria fatura mais.quantidade de itens, e não faturamento. As 3.650 vendas "Sem Categoria" precisam ser corrigidas na origem.

