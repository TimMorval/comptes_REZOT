import sys
from bank_process_utils import read_file, drop_column, replace_and_convert, calculate_debit_credit, rename_columns, save_to_csv

def process_bnp(input_name, save=True):
    data = read_file(input_name, skiprows=0, delimiter=';', encoding='ISO-8859-1')
    data = drop_column(data, "Devise")
    operations = replace_and_convert(data, "Montant de l'opération", ',', '.')
    data = drop_column(data, "Montant de l'opération")
    data["Débit"], data["Crédit"] = calculate_debit_credit(operations)
    data = rename_columns(data, {"Détail de l'écriture": "Détails"})

    if save:
        save_to_csv(data, input_name.replace('.csv', '_processed.csv'), sep=';', encoding='ISO-8859-1')
    return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_bnp.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_bnp(input_file)
