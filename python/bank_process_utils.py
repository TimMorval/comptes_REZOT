import pandas as pd

def read_file(file_path, skiprows, delimiter, encoding):
    return pd.read_csv(file_path, skiprows=skiprows, delimiter=delimiter, encoding=encoding)

def drop_column(df, column_name):
    return df.drop(column_name, axis=1)

def replace_and_convert(df, column_name, to_replace, replacement, convert_to_type=float):
    return df[column_name].str.replace(' ', '').str.replace(to_replace, replacement).astype(convert_to_type)

def calculate_debit_credit(operations):
    debit = operations.apply(lambda x: x if x < 0 else 0).astype(str).str.replace('.', ',')
    credit = operations.apply(lambda x: x if x > 0 else 0).astype(str).str.replace('.', ',')
    return debit, credit

def rename_columns(df, rename_dict):
    df.rename(rename_dict, axis=1, inplace=True)
    return df

def save_to_csv(df, output_name, sep, encoding):
    df.to_csv(output_name, index=False, sep=sep, encoding=encoding)
