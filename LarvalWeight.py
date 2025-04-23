import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_excel("/Users/seggewa/Downloads/Larval-Weight.xlsx")

palette = {
    'SI': 'yellow',
    '100': '#2F8ABF',
    '150': '#FF8A15',
    '200': '#52B152',
    '50': '#DD4E4E',
}
#target_conditions = ['SI', '100']
#data = bigdata[bigdata['Density'].isin(target_conditions)]
sns.barplot(x=data.Density, y=data.Weight, errorbar='sd', hue=data.Density, palette=palette)
sns.stripplot(data, x=data.Density, y=data.Weight, color='grey', size=6, jitter=True, alpha=.3)


plt.ylabel('Weight in mg')
plt.xlabel('Density')
plt.title('Larval weight X Density')
plt.show()  