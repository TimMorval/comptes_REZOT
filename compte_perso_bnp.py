import pandas as pd

def process_bnp(file_path):
    df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
    df = df.drop([df.columns[i] for i in [1,-1]], axis=1)
    new_df, operations =df.drop(df.columns[-1], axis=1), df[df.columns[-1]].str.replace(',', '.').str.replace(' ', '').astype(float) 
    new_df = new_df.rename({df.columns[0]:'Date operation', df.columns[1]:'Libelle operation', df.columns[2]:'Details'}, axis=1)
    new_df["Débit"] = operations.apply(lambda x: x if x < 0 else 0)
    new_df["Crédit"] = operations.apply(lambda x: x if x > 0 else 0)
    new_df["Débit"] = new_df["Débit"].astype(str).str.replace('.', ',')
    new_df["Crédit"] = new_df["Crédit"].astype(str).str.replace('.', ',')
    return new_df

def save_bnp(df, output_path):
    df.to_csv(output_path, index=False, sep=';', encoding='ISO-8859-1')