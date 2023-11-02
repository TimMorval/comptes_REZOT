import pandas as pd

def process_sg(file_path):
    df = pd.read_csv(file_path, skiprows=2, delimiter=';', encoding='ISO-8859-1')
    df = df.drop("Devise", axis=1)
    new_df, operations = df.drop("Montant de l'opération", axis=1), df["Montant de l'opération"].str.replace(',', '.').astype(float) 
    new_df.rename({"Détail de l'écriture":"Détails"}, axis=1, inplace=True)
    new_df, operations = df.drop("Montant de l'opération", axis=1), df["Montant de l'opération"].str.replace(',', '.').astype(float) 
    new_df.rename({"Détail de l'écriture":"Détails"}, axis=1, inplace=True)
    new_df["Débit"] = operations.apply(lambda x: x if x < 0 else 0)
    new_df["Crédit"] = operations.apply(lambda x: x if x > 0 else 0)
    new_df["Débit"] = new_df["Débit"].astype(str).str.replace('.', ',')
    new_df["Crédit"] = new_df["Crédit"].astype(str).str.replace('.', ',')
    return new_df

def save_sg(df, output_path):
    df.to_csv(output_path, index=False, sep=';', encoding='ISO-8859-1')