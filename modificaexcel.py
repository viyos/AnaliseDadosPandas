import pandas as pd
import scipy.stats
import numpy as np
import datetime 
from dateutil.relativedelta import relativedelta
from datetime import datetime

#Estruturação dos dados para facilitar 
def FormatExcel(Arquivo):
    tabelas_read = pd.read_csv(rf"C:\Users\victory\Downloads\{Arquivo}.csv",sep=',',encoding='utf-8')
    tabela_mod = pd.DataFrame(tabelas_read)
    tabela_mod = tabela_mod.drop('Unnamed: 0', axis = 1)
    tabela_mod = tabela_mod.dropna(how='all')
    if Arquivo == 'cases':
        tabela_mod['date_ref'] = pd.to_datetime(tabela_mod['date_ref'])
    else:
        tabela_mod.dropna(subset = ['accountid'], inplace=True)
        tabela_mod = tabela_mod.drop_duplicates()
        tabela_mod['cred_date'] = pd.to_datetime(tabela_mod['cred_date'])
#    print(tabela_mod)
#    print(tabela_mod.dtypes)
    tabela_mod.to_csv(rf"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\{Arquivo}.csv", index=False,sep=';',encoding='utf-8-sig')

lista_arquivos =['cases','creds']

for i in lista_arquivos:
    FormatExcel(i)

#Questão 1
creds = pd.read_csv(r"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\creds.csv",sep=';',encoding='utf-8')
cases = pd.read_csv(r"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\cases.csv",sep=';',encoding='utf-8')
creds = pd.DataFrame(creds)
cases = pd.DataFrame(cases)

#Quantificando cada coluna para contagem
cases['caso'] = 1
# Explicitly convert to date
cases['date_ref'] = pd.to_datetime(cases['date_ref'])
# Set your date column as index 
cases.set_index('date_ref',inplace=True) 
# For monthly use 'M', If needed for other freq you can change.

valores_antes = []
valores_depois = []

for i in range(6):
    valores_antes.append(cases['caso'].resample('M').sum()[i])
print(valores_antes)

for j in range(6,9,1):
    valores_depois.append(cases['caso'].resample('M').sum()[j])
print(valores_depois)

p_value = scipy.stats.ttest_ind(valores_antes,valores_depois)
print(p_value)
print(f"Valor médio de chamados antes é de {np.mean(valores_antes)}. \n Já a média de chamados depois da implementação é de {np.mean(valores_depois)}.")

#Como o valor de p no teste de hipotese é menor do que 0.05 e a média anterior é menor do que a média posterior a mudança, concluimos que não houve alteração depois da implementação.

#Questão 2
creds = pd.read_csv(r"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\creds.csv",sep=';',encoding='utf-8')
cases = pd.read_csv(r"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\cases.csv",sep=';',encoding='utf-8')
creds = pd.DataFrame(creds)
cases = pd.DataFrame(cases)

cases['date_ref'] = pd.to_datetime(cases['date_ref'])
creds['cred_date']= pd.to_datetime(creds['cred_date'])

#Left join entre dataframes 
left_join = cases.merge(creds, on='accountid', how='left')

left_join['Difença_dias'] = 'NaN' #abs(relativedelta(left_join['cred_date'] , left_join['date_ref']))

left_join['date_ref'] = pd.to_datetime(left_join['date_ref'])
left_join['cred_date']= pd.to_datetime(left_join['cred_date'])

for row in range(left_join[left_join.columns[0]].count()):
    ini = left_join.iloc[row,8]
    fim = left_join.iloc[row,1]
    left_join.loc[row,'Difença_dias'] = abs(relativedelta(ini, fim)).days
    left_join.loc[row,'Difença_meses'] = abs(relativedelta(ini, fim)).months
    left_join.loc[row,'Difença_anos'] = abs(relativedelta(ini, fim)).years

left_join['Difença_dias'] = left_join['Difença_dias'].astype(int)
left_join['Difença_meses'] = left_join['Difença_meses'].astype(int)
left_join['Difença_anos'] = left_join['Difença_anos'].astype(int)
left_join['Difença_meses'] = left_join['Difença_meses']*30
left_join['Difença_anos'] = left_join['Difença_anos']*365
left_join['Difença_tot_dias'] = left_join['Difença_anos'] + left_join['Difença_meses'] + left_join['Difença_dias']
left_join.to_csv(rf"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\left_join.csv", index=False,sep=';',encoding='utf-8-sig')

#Para esse caso primeiramente realizei a limpeza de alguns dados faltantes referentes ao Id dos clientes da tabela creds, pois não iriamos conseguir realizar o cruzamento desses dados com os da tabela cases.
#Logo após essa limpeza realizei o cruzamento entre as tabelas para que conseguisse visualizar a diferença entre a data de credeciamento e do registro do chamado. Após ter essas informações em uma tabela utilizei o a função relativedelta para captar a diferença de dias entre a data de credeciamento e de registro do chamado para visualizarmos a diferença notada pelo agente.

#Questão 3
cases = pd.read_csv(r"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\cases.csv",sep=';',encoding='utf-8')
cases = pd.DataFrame(cases)

#print(cases['assunto'].unique())

for row in range(cases[cases.columns[0]].count()):
    clust = cases.iloc[row,6]
    clust = str(clust)
    clust = clust.replace(':', ' ' )
    lista_clust = clust.split()
    try:
        if lista_clust[0] == 'Bandeira':
            cases.loc[row,'Cluster'] = 'Bandeiras'
        elif lista_clust[0] == 'Comunicados':
            cases.loc[row,'Cluster'] = 'Feedback'
        elif lista_clust[0] == 'Incidente':
            cases.loc[row,'Cluster'] = 'Outros'
        else:
            cases.loc[row,'Cluster'] = lista_clust[0]
    except:
        cases.loc[row,'Cluster'] = 'Outros'
#cases.to_csv(rf"C:\Users\victory\OneDrive - HDI SEGUROS SA\Área de Trabalho\Arquivos Alterados\qt3.csv", index=False,sep=';',encoding='utf-8-sig')
#print(cases['Cluster'].unique())

#Para esse caso agrupei através do assunto relacionado ao chamado nos seguintes clusters: 'Aplicativo','Produto' ,'Logística' ,'Pedido' ,'Risco' ,'Transação','Transferência' ,'Cadastro' ,'Bandeiras' ,'Feedback' ,'Outros' e 'Telecom'
#Tendo que alguns campos que possuiam poucos incidentes realizei o agrupamento em outros cluster, como o assunto 'Incidente' que entra no campo 'Outros' e 'Comunicados' que entra para o campo 'Feedback'.

#Questão 4
cases['date_ref']=pd.to_datetime(cases['date_ref'])

filtro = (cases['date_ref'] >= '2020-08-01')
df_filtro = cases[filtro]
df_filtro['Caso'] = 1
df_filtro['Semana'] = df_filtro['date_ref'].dt.to_period('W-THU')
print(df_filtro.groupby(['Cluster','Semana']).agg({'Caso':'sum'})) #Query


