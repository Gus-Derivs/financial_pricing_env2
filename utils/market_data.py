import pandas as pd

def load_rates_excel(file_path: str) -> pd.DataFrame:
    """
    Carga tasas desde un archivo Excel donde:
    - la primera fila contiene los tenores
    - la primera columna contiene las fechas
    
    Devuelve un DataFrame con fechas como índice y tenores como columnas
    """
    df = pd.read_excel(file_path, index_col=0)
    
    # Convertir índice a datetime
    df.index = pd.to_datetime(df.index)
    
    # Validación básica
    if df.isnull().values.any():
        raise ValueError("El archivo contiene valores nulos")
    
    return df