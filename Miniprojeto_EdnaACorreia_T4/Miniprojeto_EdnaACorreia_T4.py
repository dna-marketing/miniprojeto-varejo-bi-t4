# %% [markdown]
# ## Parte 1: Carregamento e visão geral da base

# %%
# Visão geral
import pandas as pd
df = pd.read_csv("Base Varejo.csv", sep=";")
df.info()


# %% [markdown]
# ## Parte 2: Diagnóstico de problemas

# %%
# Conta os valores vazios em cada coluna
print("Nulos por coluna:")
print(df.isnull().sum())

# Linhas duplicadas
print("\nLinhas duplicadas:", df.duplicated().sum())

# Categorias de produto
print("\nCategorias de produto:")
print(df["PR_CAT"].value_counts().head(10))

#Produtos: quantos nomes diferentes existem
print("\nProdutos distintos:", df["PR_NOME"].nunique())

# Datas, ver exemplos e testar se alguma é inválida
datas_convertidas = pd.to_datetime(df["DATA"], format="%d/%m/%Y")
print("\nPrimeira data:", datas_convertidas.min())
print("Última data:", datas_convertidas.max())


# %% [markdown]
# **Problemas encontrados:**
# 1. 4 colunas 10 a 13 (Unnamed) totalmente vazias
# 2. A coluna DATA está como texto, e não como data
# 3. Duplicadas: 96553
# 4. PR_CAT vendas "#N/D": 3.650 (categoria vazia disfarçada de texto)

# %% [markdown]
# ## Parte 3:	Limpeza dos dados
# 
# Aqui vou arrumar os problemas que achei na parte 2:
# - apagar as 4 colunas vazias
# - trocar o #N/D das categorias por "Sem Categoria"
# - tirar as linhas repetidas
# - mudar a coluna DATA de texto para data

# %%
# apagar as 4 colunas vazias
df = df.drop(columns=["Unnamed: 10", "Unnamed: 11", "Unnamed: 12", "Unnamed: 13"])
df.info()

# %%
# trocar o #N/D das categorias por "Sem Categoria"
def arrumar_categoria(categoria):
    if categoria == "#N/D":
        return "Sem Categoria"
    else:
        return categoria
df["PR_CAT"] = df["PR_CAT"].apply(arrumar_categoria)
print(df["PR_CAT"].value_counts().head(10))

# %% [markdown]
# Escolhi não apagar as linhas com #N/D porque são vendas de verdade, só faltava a categoria. Se apagasse, perderia 3.650 vendas. Troquei por “Sem Categoria” para não perder os dados e deixar o problema visível.

# %%
# apagar as linhas repetidas
print("\nLinhas duplicadas:", df.duplicated().sum())
df = df.drop_duplicates()
print("\nLinhas após remoção de duplicadas:", len(df))


# %%
# mudar a coluna DATA de texto para data
df["DATA"] = pd.to_datetime(df["DATA"], format='%d/%m/%Y')
df.info()



# %%
# ver quantas compras diferentes tem (CO_ID é o numero da compra)
print("\nCompras distintas:", df["CO_ID"].nunique())
print("\ntotal de itens:",len(df))



# %% [markdown]
# cada compra tem, em média 40 itens (733447/18471=40).

# %%
# salvar a base tratada em um novo arquivo CSV
df.to_csv("df_limpo.csv", sep=";", index=False)


# %% [markdown]
# ## Parte 4: Estatísticas Descritiva de “nº de filhos clientes” (CL_FHL)

# %%
# deixar so 1 linha por cliente, pra nao contar o mesmo cliente varias vezes
df_clientes = df.drop_duplicates(subset=["CL_ID"])

# estatísticas do nº filhos por cliente
print("media:", df_clientes["CL_FHL"].mean())
print("mediana:", df_clientes["CL_FHL"].median())
print("Desvio padrão:", df_clientes["CL_FHL"].std())
print("Moda:", df_clientes["CL_FHL"].mode()[0])
print("Min:", df_clientes["CL_FHL"].min())
print("Max:", df_clientes["CL_FHL"].max())
print("Contagem:", df_clientes["CL_FHL"].count())


# %% [markdown]
# Olhando os 1000 clientes, a maioria não tem filhos (a mediana e a moda deram 0). A média deu 1 filho por cliente, mas ela fica um pouco mais alta porque alguns clientes têm 3 ou 4 filhos. O mínimo é 0 e o máximo é 4 filhos. O desvio padrão de 1,4 mostra que as famílias variam bastante, tem muita gente sem filhos.

# %% [markdown]
# ## Parte 5: Agrupamentos (CL_GENERO; PR_CAT)
# Explorar padrões de agrupamento (gênero com mais vendas, compras), usando groupby() ou pivot_table().

# %%
# quantidade de itens comprados por genero
print(df.groupby("CL_GENERO")["PR_ID"].count())

# itens comprados por categoria e genero
tabela_categoria_genero = pd.pivot_table(df, index=["PR_CAT"], columns="CL_GENERO", values="PR_ID", aggfunc="count")
print(tabela_categoria_genero)



# %% [markdown]
# As mulheres compram mais, cerca de 31 mil itens a mais. Ranking das categoria: Alimentos; Higiene; Limpeza; Bebidas; Pet e Acessórios. Alimentos sozinho é mais da metade das vendas. Porém, o perfil de compra entre os gêneros não tem nenhuma discrepância.
# 

# %% [markdown]
# ## Parte 6: Conclusões

# %% [markdown]
# 1. A base tinha muitas linhas duplicadas (96.553), que teriam inflado o resultado das contagens. Depois da limpeza ficaram 733.447 itens.
# 
# 2. Optei por manter as categorias #N/D para não perder histórico de vendas e só renomeei como "Sem Categoria". Se apagasse, perderia 3.650 vendas. Assim os dados ficam e o problema continua visível.
# 
# 3. Cada compra tem, em média, 40 itens (733.447 / 18.471 = 40), parecendo compras de supermercado, tipo compra do mês.
# 
# 4. Olhando os 1000 clientes, a maioria não tem filhos (a mediana e a moda deram 0). A média deu 1 filho por cliente, mas fica um pouco mais alta porque alguns clientes têm 3 ou 4 filhos.
# 
# 5. As mulheres compram mais, cerca de 31 mil itens a mais. Ranking das categorias: Alimentos, Higiene, Limpeza, Bebidas, Pet e Acessórios. Alimentos sozinho é mais da metade das vendas, o que é natural nesse perfil de varejo. Porém, o perfil de compra entre os gêneros não tem nenhuma discrepância.
# 
# 6. A base não tem coluna de valor (R$). Dá para saber quantos itens foram vendidos, mas não quanto dinheiro entrou, então não dá para saber, por exemplo, qual categoria fatura mais. Além disso, as 3.650 vendas "Sem Categoria" precisam ser corrigidas na origem.
# 


