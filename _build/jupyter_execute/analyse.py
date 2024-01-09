#!/usr/bin/env python
# coding: utf-8

# # Résultats du sondage sur le mur de Ladoumègue

# In[1]:


import pandas  as pd
import matplotlib.pyplot as plt #librairie pour faire des graphiques
import seaborn as sns # librairie pour faire des graphiques un peu plus jolis
import plotly.express as px #librairie pour faire des graphiques interactifs


# In[2]:


df0 = pd.read_csv("/home/aymeric/python-scripts/polls_wall_ladoumegue/data/convert_mur_ladoumegue_answer.csv", sep =",")


# In[3]:


# On prend uniquement la colonne "clubs" pour compter le nombre d'individidus licenciés auprès de chaque club.
df1 = df0[["id", "Clubs"]]
df1["Clubs2"] = df1["Clubs"].apply(lambda x : x.split(','))
df1["Clubs2"] = df1["Clubs2"]
df1 = df1.explode("Clubs2")
df1["Clubs2"] = df1["Clubs2"].str.lower().str.replace(" ","")

#df1 pivot : chaque modalité de club devient une variable (colonne) binaire, 1 si licencié dans le club, 0 si non

dfp = pd.pivot_table(df1, values="Clubs2", index="id", columns= "Clubs2", aggfunc='size', fill_value="0", dropna=False)

# on fusionne le dataframe "pivoté" avec le dataframe d'origine

df = df0.merge(dfp, on = ["id"], how = "left")


# ## Les clubs d'affiliation

# In[4]:


fig, axs = plt.subplots(2, figsize=(15, 10));

dtp1 = df1.groupby(["Clubs2"]).agg(nb =("id", "size")).reset_index()
dtp1["freq"] = dtp1["nb"]/ df1.id.nunique()*100

for n, col in enumerate(["nb", "freq"]):
    sns.barplot(x = 'Clubs2', y = col, data=dtp1, ax = axs[n]);
    axs[n].set_xlabel("Clubs", fontsize = 12);
    if n == 0:
        axs[n].set_ylabel("Nombre de répondant.es", fontsize = 12);
    else:
        axs[n].set_ylabel("Proportion de répondant.es", fontsize = 12);


fig.suptitle("Les clubs d'affiliation des répondant.es (une même personne peut être inscrite dans plusieurs clubs", fontsize=16);


#fig.show()


# ## Satisfaction de la répartition des cotations

# In[5]:


d = df.groupby(["Satisfecit","level_max"]).agg(nb = ("id", "size")).reset_index()
fig = px.treemap(d, path=["Satisfecit","level_max"], values='nb')
fig


# ## Répartition des niveaux max au sein des clubs
# 
# Pour rappel, une même personne peut être licenciée de plusieurs clubs.

# In[6]:



for n, col in enumerate(df1.Clubs2.unique()):
    dtp = df.groupby([col,"level_max"]).agg(nb = (col, "sum")).reset_index()
    fig = px.treemap(dtp, path=[col,"level_max"], values='nb', title = col)
    fig.show()


# ## Satisfaction de la distribution des niveaux de voies par club.

# In[7]:



for n, col in enumerate(df1.Clubs2.unique()):
    dtp = df.groupby([col,"Satisfecit"]).agg(nb = ("id", "size")).reset_index()
    dtp = dtp.loc[dtp[col]==1]
    fig = px.treemap(dtp, path=[col,"Satisfecit"], values='nb', title = col)
    fig.show()


# ## Le niveau des répondant.es

# In[8]:


fig, axs = plt.subplots(4, figsize=(15, 15))

dtp1 = df.groupby(["level_max"]).agg(nb = ("id", "size")).reset_index()
dtp1["freq"] = dtp1["nb"]/ df.id.nunique()*100
dtp2 = df.groupby(["A_vue"]).agg(nb = ("id", "size")).reset_index()
dtp2["freq"] = dtp2["nb"]/ df.id.nunique()*100
dtp3 = df.groupby(["niveau_frequent"]).agg(nb = ("id", "size")).reset_index()
dtp3["freq"] = dtp3["nb"]/ df.id.nunique()*100
dtp4 = df.loc[df["Wish_level"]!= ""].groupby(["Wish_level"]).agg(nb = ("id", "size")).reset_index()

dtp4["freq"] = dtp4["nb"]/ df.id.nunique()*100

for n, col in enumerate([dtp2, dtp1, dtp3, dtp4]):

  if n == 0:
    sns.barplot(x = 'A_vue', y = "nb", data=col, ax = axs[n])
    axs[n].set_xlabel("Niveau à vue", fontsize = 12)
  elif n == 1:
    sns.barplot(x = 'level_max', y = "nb", data=col, ax = axs[n])
    axs[n].set_xlabel("Niveau max", fontsize = 12)
  elif n == 2:
    sns.barplot(x = 'niveau_frequent', y = "nb", data=col, ax = axs[n])
    axs[n].set_xlabel("Cotation la plus fréquente", fontsize = 12)
  else:
    sns.barplot(x = 'Wish_level', y = "nb", data=col, ax = axs[n])
    axs[n].set_xlabel("Cotation souhaitée", fontsize = 12)
  axs[n].set_ylabel("Effectif absolu", fontsize = 12)



fig.suptitle("Le niveau des répondant.es", fontsize=16);


#fig.show()


# In[ ]:




