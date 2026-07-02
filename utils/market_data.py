import pandas as pd

def load_rates_csv(file_path: str) -> pd.DataFrame:
    """
    Carga tasas desde un archivo Excel donde:
    - la primera fila contiene los tenores
    - la primera columna contiene las fechas
    
    Devuelve un DataFrame con fechas como índice y tenores como columnas
    """
    df = pd.read_csv(file_path, index_col=0)
    
    # Convertir índice a datetime
    df.index = pd.to_datetime(df.index)
    
    # Convertir columnas a numéricas
    df = df.apply(pd.to_numeric, errors='coerce')

    # Forward fill
    df = df.ffill()

    return df

df_rates = load_rates_csv(r"C:\Users\56946\Documents\financial_pricing_env2\data\raw\daily-treasury-rates.csv")

