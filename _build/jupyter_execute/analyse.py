#!/usr/bin/env python
# coding: utf-8

# # Résultats du sondage sur le mur de Ladoumègue

# In[1]:


import pandas  as pd
import matplotlib.pyplot as plt #librairie pour faire des graphiques
import seaborn as sns # librairie pour faire des graphiques un peu plus jolis
import plotly.express as px #librairie pour faire des graphiques interactifs


# In[2]:


rename_column = {
      'Horodateur':'Horodateur',
      'Au sein de quel(s) club(s) êtes-vous licencié.e ?':'Clubs',
      'Au cours des mois de novembre et décembre 2023, combien de fois approximativement avez-vous grimpé à Ladoumègue ?': 'Frequentation',
      'Aujourd’hui, quel est votre niveau à vue ? (on appelle “niveau à vue” le niveau le plus élevé des voies qu’on arrive à faire en tête au premier essai dans environ 75% des cas, quel que soit le profil et quelle que soit la salle)':'A_vue',
      'Quelle est la cotation maximale dans laquelle vous essayez des voies (en moulinette ou en tête, sans forcément enchainer la voie)':'level_max',
      'Selon vous, quel est le niveau de voie le plus fréquent sur le grand mur de Ladoumègue ?':'niveau_frequent',
      'De manière plus générale, êtes-vous satisfait.e de la répartition des niveaux ?':'Satisfecit',
      'Quel niveau aimeriez-vous rencontrer plus fréquemment ?':'Wish_level',
      "Grimperiez-vous plus souvent à Ladoumègue s'il y avait plus de voies entre :":'Wish_level2',
      'Actuellement, utilisez-vous le petit mur ?':'petit_mur',
      "Actuellement, utilisez-vous l'espace bloc?":'bloc',
      'Dans l’ensemble, j’ai trouvé que les cotations étaient':'surcotation',
      'Dans l’ensemble, j’ai trouvé que les cotations étaient ': 'coherence',
      "N'hésitez pas à utiliser le champ ci-dessous si vous souhaitez ajouter un commentaire. Vous pouvez également indiquer votre nom pour qu'on puisse revenir en discuter avec vous." : "Commentaires"
      }


# In[3]:


df0 = pd.read_csv("/home/aymeric/python-scripts/polls_wall_ladoumegue/data/convert_mur_ladoumegue_answer.csv", sep =",")


# In[4]:


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

# In[5]:



key = [k for k, v in rename_column.items() if v == 'Clubs'][0]
print(f"Question posée :  {key}")


# In[6]:


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


# ## Le niveau des répondant.es

# In[7]:


fig, axs = plt.subplots(4, figsize=(15, 30))

dtp1 = df.groupby(["level_max"]).agg(nb = ("id", "size")).reset_index()
dtp1["freq"] = dtp1["nb"]/ df.id.nunique()*100
dtp2 = df.groupby(["A_vue"]).agg(nb = ("id", "size")).reset_index()
dtp2["freq"] = dtp2["nb"]/ df.id.nunique()*100
dtp3 = df.groupby(["niveau_frequent"]).agg(nb = ("id", "size")).reset_index()
dtp3["freq"] = dtp3["nb"]/ df.id.nunique()*100
dtp4 = df.loc[df["Wish_level"]!= ""].groupby(["Wish_level"]).agg(nb = ("id", "size")).reset_index()

dtp4["freq"] = dtp4["nb"]/ df.id.nunique()*100

for n, col in enumerate([dtp2, dtp1, dtp3, dtp4]):
    fig.suptitle("Le niveau des répondant.es", fontsize=16);

    if n == 0:
        key = [k for k, v in rename_column.items() if v == "A_vue"][0]
        axs[n].set_title(key, fontsize =14)
        sns.barplot(x = 'A_vue', y = "nb", data=col, ax = axs[n])
        axs[n].set_xlabel("Niveau à vue", fontsize = 12)
        
    elif n == 1:
        key = [k for k, v in rename_column.items() if v == "level_max"][0]
        axs[n].set_title(key, fontsize =14)
        sns.barplot(x = 'level_max', y = "nb", data=col, ax = axs[n])
        axs[n].set_xlabel("Niveau max", fontsize = 12)
        
    elif n == 2:
        key = [k for k, v in rename_column.items() if v == "niveau_frequent"][0]
        axs[n].set_title(key, fontsize =14)
        sns.barplot(x = 'niveau_frequent', y = "nb", data=col, ax = axs[n])
        axs[n].set_xlabel("Cotation la plus fréquente", fontsize = 12)
    else:
        key = [k for k, v in rename_column.items() if v == "Wish_level"][0]
        axs[n].set_title(key, fontsize =14)
        sns.barplot(x = 'Wish_level', y = "nb", data=col, ax = axs[n])
        axs[n].set_xlabel("Cotation souhaitée", fontsize = 12)
    axs[n].set_ylabel("Effectif absolu", fontsize = 12)





#fig.show()


# ## Répartition des niveaux à vue au sein des clubs
# 
# Pour rappel, une même personne peut être licenciée de plusieurs clubs.

# In[8]:


key = [k for k, v in rename_column.items() if v == "A_vue"][0]
print(key)

for n, col in enumerate(df1.Clubs2.unique()):
    dtp = df.groupby([col,"A_vue"]).agg(nb = (col, "sum")).reset_index()
    fig = px.treemap(dtp, path=[col,"A_vue"], values='nb', title = f"Les niveaux à vue des adhérent.es de {col}")
    fig.show()


# ## Répartition des niveaux max au sein des clubs
# 

# In[9]:


key = [k for k, v in rename_column.items() if v == "level_max"][0]
print(key)

for n, col in enumerate(df1.Clubs2.unique()):
    dtp = df.groupby([col,"level_max"]).agg(nb = (col, "sum")).reset_index()
    fig = px.treemap(dtp, path=[col,"level_max"], values='nb', title = f"Les niveaux max des adhérent.es de {col}")
    fig.show()


# ## Satisfaction de la répartition des cotations
#  
#  ### Satisfaction en fonction du niveau à vue

# In[10]:


key1 = [k for k, v in rename_column.items() if v == "Satisfecit"][0]
key2 = [k for k, v in rename_column.items() if v == "A_vue"][0]
print(f"Croisement des questions suviantes : ")
print(f"1) {key1}")
print(f"2) {key2}")


d = df.groupby(["Satisfecit","A_vue"]).agg(nb = ("id", "size")).reset_index()
fig = px.treemap(d, path=["Satisfecit","A_vue"], values='nb', title = "La satisfaction et le niveau à vue")
fig


# ### Satisfaction en fonction du niveau max

# In[11]:


key1 = [k for k, v in rename_column.items() if v == "Satisfecit"][0]
key2 = [k for k, v in rename_column.items() if v == "level_max"][0]
print(f"Croisement des questions suviantes : ")
print(f"1) {key1}")
print(f"2) {key2}")

d = df.groupby(["Satisfecit","level_max"]).agg(nb = ("id", "size")).reset_index()
fig = px.treemap(d, path=["Satisfecit","level_max"], values='nb', title = "La satisfaction et le niveau max")
fig


# ### Satisfaction de la distribution des niveaux de voies par club.

# In[12]:


key1 = [k for k, v in rename_column.items() if v == "Satisfecit"][0]

print(key1)

for n, col in enumerate(df1.Clubs2.unique()):
    dtp = df.groupby([col,"Satisfecit"]).agg(nb = ("id", "size")).reset_index()
    dtp = dtp.loc[dtp[col]==1]
    fig = px.treemap(dtp, path=[col,"Satisfecit"], values='nb', title = col)
    fig.show()


# ## Les personnes non satisfaites
#  
#  ### Les personnes non satisfaites et le niveau qu'elles souhaitent rencontrer plus souvent

# In[13]:


key1 = [k for k, v in rename_column.items() if v == "Wish_level"][0]

print(key1)
df2 = df.loc[df["Satisfecit"]=="Non"]


dtp = df2.groupby(["Satisfecit", "Wish_level"]).agg(nb = ("id", "size")).reset_index()
#dtp = dtp.loc[dtp[col]==1]
fig = px.treemap(dtp, path=["Satisfecit", "Wish_level"], values='nb')
fig.show()


# ### Les personnes non satisfaites et le niveau qu'elles souhaitent rencontrer plus souvent en fonction du club

# In[14]:


key1 = [k for k, v in rename_column.items() if v == "Wish_level"][0]

print(key1)
df2 = df.loc[(df["Satisfecit"]=="Non")]
df2 = df2.loc[~df2["Satisfecit"].isna()]

for n, col in enumerate(df1.Clubs2.unique()):
    dtp = df2.groupby([col,"Wish_level"]).agg(nb = ("id", "size")).reset_index()
    dtp = dtp.loc[dtp[col]==1]
    if len(dtp)> 0 :
        fig = px.treemap(dtp, path=[col,"Wish_level"], values='nb', title = col)
        fig.show()
    else:
        pass


# In[ ]:




