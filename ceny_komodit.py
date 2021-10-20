#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

start_date = '2021-01-01'
end_date_dt = pd.Timestamp.today() - pd.Timedelta(value=2, unit='D')
end_date = end_date_dt.strftime('%Y-%m-%d')

bushel_corn = .0254
bushel_wheat = .0272155
bushel_soybean = .0272155


# Zdroj: https://pypi.org/project/yfinance/
# 
# Komodity: https://finance.yahoo.com/commodities
# 
# EUR/USD: https://finance.yahoo.com/currencies


from pandas_datareader import data as pdr

corn_1 = pdr.get_data_yahoo('ZC=F', start=start_date, end=end_date)
wheat_1 = pdr.get_data_yahoo('KE=F', start=start_date, end=end_date)
soybean_1 = pdr.get_data_yahoo('ZS=F', start=start_date, end=end_date)
soy_meal_1 = pdr.get_data_yahoo('ZM=F', start=start_date, end=end_date)

fx = pdr.get_data_yahoo('EURUSD=X', start=start_date, end=end_date)

# fx_last = fx.tail(1).iloc[0,3]


commodities = pd.DataFrame()
commodities['Kukuřice'] = corn_1['Close']/bushel_corn/100/fx['Close']
commodities['Pšenice'] = wheat_1['Close']/bushel_wheat/100/fx['Close']
commodities['Soja'] = soybean_1['Close']/bushel_soybean/100/fx['Close']
commodities['Sojový šrot'] = soy_meal_1['Close']/fx['Close']

commodities['Krmivo'] = 0.3 * commodities['Sojový šrot'] + 0.35 * commodities['Kukuřice'] + 0.35 * commodities['Pšenice']

commodities.fillna(method='ffill', inplace=True)

ft = 'Calibri'

pozadi = '#EAE7DC'
barva1 = '#8E8DBA'
barva2 = '#E85A4F'
barva3 = '#D8C3A5'
barva4 = '#E98074'

x = commodities.index.strftime('%d') + ' ' + commodities.index.strftime('%b') + ' ' + commodities.index.strftime('%y')

graf_obil = plt.figure(figsize = (10, 5), facecolor = pozadi)

ax_obil = graf_obil.add_axes([0,0,1,1])

ax_obil.plot(x, commodities['Kukuřice'], color = barva1, linewidth=3)
ax_obil.plot(x, commodities['Pšenice'], color = barva2, linewidth=3)

ax_obil.set_title('Vývoj cen kukuřice a pšenice', fontsize = 24, fontname = ft)
ax_obil.set_ylabel('Cena (€/t)', fontsize = 14)
ax_obil.set_xlabel('Den', fontsize = 14)
ax_obil.grid(color = '0.5', ls='-.', lw=0.25)
ax_obil.legend(labels = ['Kukuřice', 'Pšenice'], fontsize = 14)
plt.xticks(np.arange(0, len(commodities), step=30))
# plt.savefig('obilniny EUR.png', dpi = 300, bbox_inches='tight', facecolor = pozadi)
plt.show()

graf_soja = plt.figure(figsize = (10, 5), facecolor = pozadi)

ax_soja = graf_soja.add_axes([0,0,1,1])

ax_soja.plot(x, commodities['Soja'], color = barva3, linewidth=3)
ax_soja.plot(x, commodities['Sojový šrot'], color = barva4, linewidth=3)

ax_soja.set_title('Vývoj cen sóji', fontsize = 24, fontname = ft)
ax_soja.set_ylabel('Cena (€/t)', fontsize = 14)
ax_soja.set_xlabel('Den', fontsize = 14)
ax_soja.grid(color = '0.5', ls='-.', lw=0.25)
ax_soja.legend(labels = ['Sója', 'Sojový šrot'], fontsize = 14)
plt.xticks(np.arange(0, len(commodities), step=30))
# plt.savefig('soja EUR.png', dpi = 300, bbox_inches='tight', facecolor = pozadi)
plt.show()


graf_krm = plt.figure(figsize = (10, 5), facecolor = pozadi)

ax_krm = graf_krm.add_axes([0,0,1,1])

ax_krm.plot(x, commodities['Krmivo'], color = barva1, linewidth=4)

ax_krm.set_title('Vývoj cen generického krmiva', fontsize = 24, fontname = ft)
ax_krm.set_ylabel('Cena (€/t)', fontsize = 14)
ax_krm.set_xlabel('Den', fontsize = 14)
ax_krm.grid(color = '0.5', ls='-.', lw=0.25)
ax_krm.legend(labels = ['Krmivo'], fontsize = 14)
plt.xticks(np.arange(0, len(commodities), step = 30))
# plt.savefig('krmivo EUR.png', dpi = 300, bbox_inches='tight', facecolor = pozadi)
plt.show()

expl = '''
**"Generické krmivo"** se skládá z:
- 30 procent sojového šrotu,
- 30 procent pšenice,
- 35 procent kukuřice.
'''

st.title('Ceny komodit na burze')
st.text('\n')
st.markdown(expl)
st.text('\n')
st.pyplot(graf_obil)
st.text('\n')
st.pyplot(graf_soja)
st.text('\n')
st.pyplot(graf_krm)





