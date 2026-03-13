import pandas as pd


def load_mybrains_excel(file):

    df = pd.read_excel(file, header=None)

    header1 = df.iloc[1]
    header2 = df.iloc[2]

    header2 = header2.fillna(header1)
    header2 = header2.replace("", pd.NA).fillna(header1)

    df.columns = header2

    df = df.iloc[3:].reset_index(drop=True)

    df = df.iloc[:-1]

    return df
