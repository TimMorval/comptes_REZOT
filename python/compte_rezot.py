import pandas as pd
import re
import sys
from bank_process_utils import drop_column, save_to_csv

def process_file(input_file, output_file):

    def search(text):
        pers_pattern = r'[POUR|DE]: (\w*) (\w*)'
        match_pers = re.search(pers_pattern, text, re.IGNORECASE)
        if re.search('railway', text, re.IGNORECASE):
            return 'Railway'
        if re.search('google', text, re.IGNORECASE):
            return 'Google'
        if re.search('FACEBK', text, re.IGNORECASE):
            return 'FACEBOOK'
        if re.search('LinkedIn', text, re.IGNORECASE):
            return 'LINKEDIN'
        if re.search('webflow', text, re.IGNORECASE):
            return 'Webflow'
        if re.search('SNCF', text, re.IGNORECASE):
            return 'SNCF'
        if re.search('RATP', text, re.IGNORECASE):
            return 'RATP'
        if re.search('GITHUB', text, re.IGNORECASE):
            return 'GITHUB'
        if re.search('SENTRY', text, re.IGNORECASE):
            return 'SENTRY'
        if re.search('FIGMA', text, re.IGNORECASE):
            return 'FIGMA'
        if re.search('TOTAL', text, re.IGNORECASE):
            return 'TOTAL'
        if re.search('SG', text, re.IGNORECASE):
            return 'SG'
        if re.search('GAB', text, re.IGNORECASE):
            return 'SG'
        if match_pers:
            groups = match_pers.groups()
            if groups[1] == 'ID':
                return groups[0]
            else:
                return ' '.join(groups)
        return 'Autre'

    def extract_for(data):
        index = data[data.Date.notna()].index
        texts = data["Nature de l'opération"].tolist()
        result = []
        for i in range(len(index)):
            if i == len(index)-1:
                text = ' '.join(texts[index[i]:])
                result.append(search(text))
            else:
                text = ' '.join(texts[index[i]:index[i+1]])
                result.append(search(text))
        return result

    # Function to get main dataframe

    def get_data(data):
        date_not_na = data.Date.notna()
        df = drop_column(data[date_not_na], 'Devise')
        df = drop_column(df, 'Date de valeur')
        df["Débit"] = df.Débit.fillna("0").str.replace(' ', '')
        df["Crédit"] = df.Crédit.fillna("0").str.replace(' ', '')
        df['POUR/DE'] = extract_for(data)
        return df.reset_index(drop=True)

    # Function to handle 'COMMISSIONS ET FRAIS DIVERS'

    def commission(df):
        lib = df['Libellé interbancaire'].tolist()
        for i, text in enumerate(lib):
            if text == 'COMMISSIONS ET FRAIS DIVERS':
                df.loc[i, 'POUR/DE'] = 'SG'
        return df

    # Read the input CSV file
    data = pd.read_csv(input_file, skiprows=6, delimiter=';')

    # Process the data
    df = get_data(data)
    df = commission(df)

    save_to_csv(df, output_file, sep=';', encoding='ISO-8859-1')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compte.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_file(input_file, output_file)
