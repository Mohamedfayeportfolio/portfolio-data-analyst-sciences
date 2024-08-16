#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[63]:


# Charger le fichier Excel
#"Let's load the Excel file"
df = pd.read_excel('supply chain retail.xlsx', engine='openpyxl')


# In[65]:


df.head()


# In[67]:


df.shape


# In[69]:


df.head()


# In[6]:


df.isnull().sum()


# In[7]:


# Convertir les dates en format DateTime
#"Convert dates to DateTime format"
df['Date'] = pd.to_datetime(df['Date'])


# In[8]:


# Analyse desciptive du jeu de données
#"Descriptive analysis of the dataset"
df.describe()


# In[9]:


# Relation entre les variables quantitatives
#"Relationship between quantitative variables"
sns.pairplot(df)


# In[10]:


# Calculons le taux de service client
#"Let's calculate the customer service rate"
df['Taux_Service_Client'] = (df['Commandes_Livrees_A_Temps'] / df['Commandes_Totales']) * 100


# In[11]:


# Afficher les premières lignes pour vérifier le calcul
#"Display the first rows to verify the calculation"
print(df[['Date', 'Taux_Service_Client']].head())


# In[12]:


# Visualisons le taux de service client au fil du temps
#"Visualize the customer service rate over time"
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Taux_Service_Client'], marker='o')
plt.title('Taux de Service Client')
plt.xlabel('Date')
plt.ylabel('Taux de Service Client (%)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# In[13]:


# Ajoutons des colonnes pour le mois et l'année
#"Add columns for the month and year"
df['Mois'] = df['Date'].dt.to_period('M')
df['Année'] = df['Date'].dt.year


# In[14]:


df.head()


# Calculons les Moyennes Mensuelles et Annuelles

# In[16]:


# Moyenne mensuelle du taux de service client
#"Monthly average of the customer service rate"
df_mensuel = df.groupby('Mois')['Taux_Service_Client'].mean().reset_index()

# Moyenne annuelle du taux de service client
#"Annual average of the customer service rate"
df_annuel = df.groupby('Année')['Taux_Service_Client'].mean().reset_index()


# In[17]:


# Afficher la moyenne mensuelle du taux de service client
#"Display the monthly average of the customer service rate"
print("Moyenne Mensuelle du Taux de Service Client :")
print(df_mensuel)

# Afficher la moyenne annuelle du taux de service client
#"Display the annual average of the customer service rate"
print("\nMoyenne Annuelle du Taux de Service Client :")
print(df_annuel)


# Graphique Mensuel

# In[19]:


# Visualisation les moyennes mensuelles du taux de service client
#"Visualize the monthly averages of the customer service rate"
plt.figure(figsize=(12, 6))
plt.plot(df_mensuel['Mois'].astype(str), df_mensuel['Taux_Service_Client'], marker='o', linestyle='-', color='b')
plt.title('Moyenne Mensuelle du Taux de Service Client')
plt.xlabel('Mois')
plt.ylabel('Taux de Service Client (%)')
plt.xticks(rotation=45)  # Rotation des labels des mois pour une meilleure lisibilité
plt.grid(True)
plt.tight_layout()
plt.show()


# Graphique Annuel

# In[21]:


# Visualisons les moyennes annuelles du taux de service client
#"Visualize the annual averages of the customer service rate"
plt.figure(figsize=(12, 6))
plt.plot(df_annuel['Année'], df_annuel['Taux_Service_Client'], marker='o', linestyle='-', color='g')
plt.title('Moyenne Annuelle du Taux de Service Client')
plt.xlabel('Année')
plt.ylabel('Taux de Service Client (%)')
plt.grid(True)
plt.tight_layout()
plt.show()


#  Analyse des Tendances

# In[23]:


df_mensuel['Mois'] = df_mensuel['Mois'].dt.to_timestamp()


# In[24]:


# Visualisons les moyennes mensuelles du taux de service client
#"Let's visualize the monthly averages of the customer service rate"
plt.figure(figsize=(12, 6))
plt.plot(df_mensuel['Mois'], df_mensuel['Taux_Service_Client'], marker='o', linestyle='-', color='b')
plt.title('Moyenne Mensuelle du Taux de Service Client')
plt.xlabel('Mois')
plt.ylabel('Taux de Service Client (%)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


#  Identifions les Périodes de Performances Particulièrement Bonnes ou Mauvaises

# In[26]:


# Trouvons les mois avec les meilleures et les pires performances
#"Find the months with the best and worst performance"
meilleure_performance_mois = df_mensuel.loc[df_mensuel['Taux_Service_Client'].idxmax()]
pire_performance_mois = df_mensuel.loc[df_mensuel['Taux_Service_Client'].idxmin()]

print("Meilleure Performance Mensuelle:")
print(meilleure_performance_mois)

print("\nPire Performance Mensuelle:")
print(pire_performance_mois)


# analyser les différentes composantes d'une série temporelle

# In[28]:


from statsmodels.tsa.seasonal import seasonal_decompose

# Décomposer les séries temporelles
#"Decompose the time series"
df.set_index('Date', inplace=True)
decomposition = seasonal_decompose(df['Taux_Service_Client'], model='additive')

# Visualiser la décomposition
plt.figure(figsize=(14, 10))
plt.subplot(4, 1, 1)
plt.plot(decomposition.observed)
plt.title('Observé')

plt.subplot(4, 1, 2)
plt.plot(decomposition.trend)
plt.title('Tendance')

plt.subplot(4, 1, 3)
plt.plot(decomposition.seasonal)
plt.title('Saisonnier')

plt.subplot(4, 1, 4)
plt.plot(decomposition.resid)
plt.title('Résidu')

plt.tight_layout()
plt.show()


#  Calcul des Délais de Livraison

# In[30]:


# Exemple de données
data = {
    'Date_Commande': ['2024-07-01', '2024-07-03', '2024-07-05', '2024-07-10', '2024-07-12'],
    'Date_Livraison': ['2024-07-06', '2024-07-08', '2024-07-10', '2024-07-15', '2024-07-18'],
    'Commandes_Totales': [100, 150, 200, 250, 300],
    'Commandes_Livrees_A_Temps': [95, 140, 190, 240, 290]
}

# Création du DataFrame initial
df1 = pd.DataFrame(data)

# Convertir les dates en format DateTime
df1['Date_Commande'] = pd.to_datetime(df1['Date_Commande'])
df1['Date_Livraison'] = pd.to_datetime(df1['Date_Livraison'])

# Calculer le délai de livraison en jours
df1['Delai_Livraison'] = (df1['Date_Livraison'] - df1['Date_Commande']).dt.days

# Renommer le DataFrame de df à df1
df1 = df1.copy()

# Afficher le DataFrame df1 pour vérifier
print(df1)


# 5. Analyse des Causes des Retards
# Examine les données pour identifier les patterns de retard, comme par région ou type de produit si ces informations sont disponibles.

# In[32]:


regions = ['Nord', 'Sud', 'Nord', 'Ouest', 'Est'] * (len(df1) // 5) + ['Nord', 'Sud', 'Nord', 'Ouest', 'Est'][:len(df) % 5]
df1['Région'] = regions


# In[33]:


#Attribuer une seule valeur à toutes les lignes
#Si vous voulez attribuer une seule région à toutes les lignes, vous pouvez le faire en une seule instruction
df1['Région'] = 'Nord'


# In[34]:


#Utiliser des valeurs aléatoires pour remplir la colonne
#Si vous voulez attribuer aléatoirement une des régions à chaque ligne
import numpy as np

df1['Région'] = np.random.choice(['Nord', 'Sud', 'Ouest', 'Est'], size=len(df1))


# In[35]:


# Manuellement définir les valeurs
#Si vous voulez spécifier manuellement les régions pour les premières 5 lignes et laisser les autres valeurs vides ou en les remplissant par une valeur spécifique
df1['Région'] = ['Nord', 'Sud', 'Nord', 'Ouest', 'Est'] + ['Valeur par défaut'] * (len(df1) - 5)


# In[36]:


#Après avoir ajouté la colonne Région, vous pouvez relancer votre analyse par région 
#"After adding the Region column, you can restart your analysis by region"
df1_region = df1.groupby('Région')['Delai_Livraison'].describe()
print(df1_region)


# In[37]:


df1


# In[38]:


# Exemple de données
data = {
    'Région': ['Nord', 'Sud', 'Est', 'Ouest', 'Nord', 'Sud', 'Est', 'Ouest'],
    'Delai_Livraison': [5, 6, 7, 5, 6, 4, 6, 5]
}


# In[39]:


df = pd.DataFrame(data)

# Vérifier les colonnes
print(df.columns)


# In[40]:


print(df.head())  # Affiche les premières lignes du DataFrame


# In[41]:


# Créer un graphique en barres
plt.figure(figsize=(10, 6))
df.groupby('Région')['Delai_Livraison'].mean().plot(kind='bar', color='skyblue')

# Ajouter des labels et un titre
plt.xlabel('Région')
plt.ylabel('Délai de Livraison (jours)')
plt.title('Délai de Livraison Moyen par Région')
plt.xticks(rotation=0)

# Afficher le graphique
plt.show()


# In[42]:


df.head()


# In[43]:


df1.head(10)


# In[59]:


# Recommandations basées sur les analyses
recommandations = """
4. Recommandations et Optimisations 🚀

Mohamed : "Enfin, basons-nous sur ces analyses pour proposer des recommandations. Voici ce que je suggère :"

1. **Réduire les délais de livraison** en optimisant les processus logistiques, notamment en travaillant avec des transporteurs plus rapides ou en ajustant les horaires de préparation des commandes.
2. **Améliorer le taux de service client** en analysant de manière plus détaillée les causes des retards et en mettant en place des actions correctives.
3. **Mettre en place un système d'alerte** pour identifier rapidement les commandes à risque de retard, afin d'intervenir avant que le délai de livraison soit dépassé.
4. **Optimiser la gestion des stocks** en se basant sur les tendances de ventes saisonnières pour éviter les ruptures de stock et les surstocks.
5. **Améliorer la communication inter-départements** pour une meilleure coordination entre les équipes de vente, logistique et approvisionnement.

"""


# In[61]:


# Affichage des recommandations
print(recommandations)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




