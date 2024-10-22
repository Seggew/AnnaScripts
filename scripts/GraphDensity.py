import os
import pandas as pd
import matplotlib.pyplot as plt

input_dir = '/Users/seggewa/Desktop/DataAnalysis/BodyLengthDensity.xlsx'

data = pd.read_excel(input_dir)

print(data.head())

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.bar(data['Density'], data['BodyLength'])
plt.xlabel('Density')
plt.ylabel('BodyLength')
plt.title('Density on body length')

plt.subplot(1, 2, 2)
plt.plot(data['Density'], data['BodyLength'], marker='o', linestyle='-')
plt.xlabel('Density')
plt.ylabel('BodyLength')
plt.title('Density on body length')

plt.tight_layout()
plt.show()