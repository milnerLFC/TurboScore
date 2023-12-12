import numpy as np
import pandas as pd

def table (probh,probd,proba,meta_test,meta_pred,min_entropy,max_entropy):

    dataframe = pd.DataFrame({
        'Home': probh,
        'Draw': probd,
        'Away': proba
    })


    dataframe['pred'] = np.where((dataframe['Draw'] > dataframe['Home']) & (dataframe['Draw'] > dataframe['Away']), 'D',
                                np.where(dataframe['Home'] > dataframe['Away'], 'H', 'A'))

    dataframe = pd.concat([pd.concat([meta_test,meta_pred]).reset_index(drop=True), dataframe], axis=1)

    dataframe['prop entropy'] = dataframe[['Home', 'Draw', 'Away']].apply(lambda x: (-np.sum(x * np.log2(x + 1e-12))-min_entropy)/ (max_entropy-min_entropy), axis=1)
    dataframe['Bprob'] = dataframe[['Home', 'Draw', 'Away']].max(axis=1)
    dataframe['Odd'] = np.where(dataframe['pred'] == 'H', dataframe['PSH'],
                                    np.where(dataframe['pred'] == 'D', dataframe['PSD'], dataframe['PSA']))
    # dataframe['DateTime'] = pd.to_datetime(dataframe['Date'] + ' ' + dataframe['Time'], format='%d/%m/%Y %H:%M')

    # dataframe = dataframe.sort_values(by='DateTime')
    # dataframe['Date'] = pd.to_datetime(dataframe['Date'], format='%d/%m/%Y')
    # dataframe.sort_values(by='Date', inplace=True)
    return dataframe
    

def table_filter(dataframe, test_size, oddmin, bprobmin):
    filtered_df = dataframe.head(test_size).sort_values('Bprob',ascending=False).copy()
    filtered_df = filtered_df[filtered_df['Odd']>oddmin]
    filtered_df = filtered_df[(filtered_df['Bprob']>bprobmin) & (filtered_df['Bprob']<.95)]
    
    return filtered_df

def table_bet (dataframe,bet_amount_base):
    dataframe['base_bet'] = bet_amount_base * (1+dataframe['Bprob'])

    for index, row in dataframe.iterrows():
        prediction = row['pred']
        true_result = row['FTR']
        dataframe.at[index, 'potential'] = row['base_bet'] * (row['Odd'] - 1)
        
        dataframe.at[index, 'result'] = dataframe.at[index,'potential']
        if  prediction != true_result:
            dataframe.at[index, 'result'] = -row['base_bet']
    
    return dataframe


def table_pred (dataframe, tail_size):
    return  dataframe[(dataframe['FTHG'].isna()) & (dataframe['FTAG'].isna()) & (dataframe['FTR'].isna())][['DateTime','HomeTeam','AwayTeam','pred','PSH','PSD','PSA','Home','Draw','Away','prop entropy','Bprob','Odd','base_bet','potential']].copy().tail(tail_size)