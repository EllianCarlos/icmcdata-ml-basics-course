import re                          # Expressão regulares
import requests                    # Acessar páginas da internet
from bs4 import BeautifulSoup      # Raspar elementos de páginas da internet
import pandas as pd                # Abrir e concatenar bancos de dados
import seaborn as sns
import matplotlib.pyplot as plt

def read_cartola_data(year):
    '''
    Read data from a given year of the CaRtola repository

    Parameters:
    year (int) - year inside the range 2018-2020.
    ''' 

    if year in [2018, 2019, 2020]:

        # URL para baixar os arquivos
        url = 'https://github.com/henriquepgomide/caRtola/tree/master/data/{}'.format(year)
        html = requests.get(url)
    
        soup = BeautifulSoup(html.text, 'lxml')
    
        dict_of_files = {}
        for tag in soup.find_all('a', attrs={'href': re.compile('rodada-([0-9]|[0-9][0-9])\.csv')}):
            href_str = tag.get('href')
            file_name = re.sub('/henriquepgomide/caRtola/blob/master/data/{}/'.format(year), 
                            '', 
                            href_str)
            
            file_url = re.sub('/henriquepgomide/caRtola/blob/master/data/{}/'.format(year), 
                            'https://raw.githubusercontent.com/henriquepgomide/caRtola/master/data/{}/'.format(year), 
                            href_str)
            dict_of_files[file_name] = file_url
    
        list_of_dataframes = []
        for key, item in dict_of_files.items():
            df = pd.read_csv(item)
            df['rodada'] = key
            list_of_dataframes.append(df)
    
        df_cartola = pd.concat(list_of_dataframes)
    
        return df_cartola
    
    else:
        print('You need to add an year within the range: 2018 and 2020')

if __name__ == "__main__":
    df = read_cartola_data(2020)
    df = df.drop(["Unnamed: 0"], axis=1)
    print(df.dtypes)
    players_more_than_18 = df.groupby(['atletas.atleta_id', 'atletas.status_id'])['atletas.status_id'].count()
    players_more_than_18 = players_more_than_18.xs('Provável', level='atletas.status_id')
    players_more_than_18 = players_more_than_18[players_more_than_18 >= 18].index.tolist()

    df_players_more_than_18 = df[['atletas.slug', 'atletas.atleta_id']].copy()
    df_players_more_than_18 = df_players_more_than_18[df_players_more_than_18['atletas.atleta_id'].isin(players_more_than_18)].drop_duplicates()

    dict_of_players_more_than_18 = df_players_more_than_18.set_index('atletas.atleta_id').to_dict()['atletas.slug']
    top_df = df[(df['atletas.posicao_id'] != 'tec') & (df['atletas.atleta_id'].isin(dict_of_players_more_than_18))]
    sns.histplot(top_df["atletas.media_num"])
    plt.show()
