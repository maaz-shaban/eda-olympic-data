import pandas as pd



def preprocessor(df, df_regions):
    
    df = df[df['Season'] == 'Summer']
    df = df.merge(df_regions, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df