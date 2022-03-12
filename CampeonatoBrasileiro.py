# %%
import pandas as pd
import requests
import logging
from os.path import exists


def set_up_log(root_name: str) -> None: 
    logging.root = logging.getLogger(root_name)
    logging.basicConfig(level = logging.INFO)


#If we want show a log in display
set_up_log('CampeonatoBrasileiro')

# Ler alguma tabela de algum site na web
url = requests.get("https://www.uol.com.br/esporte/futebol/campeonatos/brasileirao/")

if(url.status_code == 404):
    raise Exception("No table was found, check URL address")
elif(url.status_code == 500):
    raise Exception("Server not available")
else:
    uol = pd.read_html(url.text)
    # Exibir a quantidade de tabelas encontradas na pagina 
    #print(f'Total tables: {len(uol)}')

# Exibe a tabela encontrada pelo index
#display(uol[1])

# %%
# Obtendo os dataframes
times_campeonato = uol[0]
classificacao_campeonato = uol[1]

# Unindo os dois dataframes
times_campeonato = times_campeonato.join(classificacao_campeonato)


# %%
# Tirando o numero e o caractere especial
times_campeonato_formated = times_campeonato.classificação.str.replace('\d+\°+', '', regex=True)

# Transformando uma series em um dataframe pandas
times_campeonato = pd.DataFrame(times_campeonato_formated)

# Unindo os dois dataframes
times_campeonato = times_campeonato.join(classificacao_campeonato)

# Exibindo com a juncao 
#times_campeonato

# %%
times_campeonato_classificação_to_list = times_campeonato.classificação.tolist()

sigla = []
time = []

for clube in times_campeonato_classificação_to_list:
    sigla.append(clube[-3:])
    time.append(clube[:-3])

# %%
#Executar esse bloco apenas se for a primeira vez

sigla = pd.DataFrame(sigla, columns=['Sigla'])
time = pd.DataFrame(time, columns=['Clube'])
times_campeonato = times_campeonato.join(sigla)
times_campeonato = times_campeonato.join(time)
times_campeonato = times_campeonato[['classificação', 'Clube', 'Sigla', 'PG', 'J', 'V', 'E', 'D', 'GC', 'GP', 'SG', '%']]

# %%
times_campeonato = times_campeonato[['Clube', 'Sigla', 'PG', 'J', 'V', 'E', 'D', 'GC', 'GP', 'SG', '%']] 

# Exibe com as novas colunas
times_campeonato

# %%
# Comecando com index do 1 pela primeira vez
# Nao executar mais de uma vez, senao o indice vai auto incrementar
times_campeonato.index += 1

# Exibe dataframe
times_campeonato


# %%
# Exportar para um txt
txtFile = times_campeonato.to_csv(r'CampeonatoBrasileiro_2022.txt', header=True, index=True, sep=' ', mode='a')

# Exportar para um Excel
xlsxFile = times_campeonato.to_excel(r'CampeonatoBrasileiro_2022.xlsx', header=True, index=True)

# %%
# Verifica se ambos arquivos existem no classpath 
file_txt_exists = exists("CampeonatoBrasileiro_2022.txt")
file_xlsx_exists = exists("CampeonatoBrasileiro_2022.xlsx")

# %%
if(file_txt_exists and file_xlsx_exists):
    logging.info('The files txt and xlsx are crated with success in the directory')  
elif(file_txt_exists or file_xlsx_exists):
    logging.info('Only one file was created, check the directory')  
else:
    logging.info('There are no files created in the directory')  


