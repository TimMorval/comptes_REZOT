# Imports

from tkinter import filedialog
from tkinter import Tk
import pandas as pd
import sys
import os
import re

# Functions

def search(text):
    pers_pattern = r'[POUR|DE]: (\w*) (\w*)'
    match_pers = re.search(pers_pattern, text, re.IGNORECASE)
    if re.search('railway', text, re.IGNORECASE):
        return 'Railway'
    if re.search('google', text, re.IGNORECASE):
        return 'Google'
    if re.search('webflow', text, re.IGNORECASE):
        return 'Webflow'
    if re.search('SNCF', text, re.IGNORECASE):
        return 'SNCF'
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
    index = data[data['Date'].notna()].index
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


def get_data(data):
    df = data[data['Date'].notna()][['Date', "Nature de l'opération",
                                     "Débit", "Crédit", "Libellé interbancaire"]]
    df[["Débit", "Crédit"]] = df[["Débit", "Crédit"]].fillna(0)
    df['POUR/DE'] = extract_for(data)
    return df.reset_index(drop=True)


def commission(df):
    lib = df['Libellé interbancaire'].tolist()
    for i, text in enumerate(lib):
        if text == 'COMMISSIONS ET FRAIS DIVERS':
            df.loc[i, 'POUR/DE'] = 'SG'
    return df

# Main

def main():
    root = Tk()
    root.withdraw()  # Hide the main window

    # Show file dialog and get the selected file path
    input_file_path = filedialog.askopenfilename(title="Select the CSV file", filetypes=[("CSV files", "*.csv")])
    if not input_file_path:
        print("No file selected. Exiting.")
        sys.exit(1)

    # Show folder dialog and get the selected folder path
    output_directory = filedialog.askdirectory(title="Select the output directory")
    if not output_directory:
        print("No directory selected. Exiting.")
        sys.exit(1)

    saving_path = os.path.join(output_directory, 'accounting.xlsx')

    data = pd.read_csv(input_file_path, skiprows=6, delimiter=';')
    df = get_data(data)
    df = commission(df)

    with pd.ExcelWriter(saving_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='sheet', index=False)

if __name__ == "__main__":
    main()
