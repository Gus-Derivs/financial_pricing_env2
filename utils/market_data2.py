
import pandas as pd
from pathlib import Path


def load_and_process_rates(file_path: str) -> pd.DataFrame:

    # Load CSV
    df = pd.read_csv(file_path, index_col=0)

    # Convert index to datetime
    df.index = pd.to_datetime(df.index)

    # Convert all columns to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # Fill missing values
    df = df.ffill()

    # Output folder
    output_folder = Path(
        r"C:\Users\56946\Documents\financial_pricing_env2\data\processed"
    )

    # Create folder if it does not exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Output file path
    output_file = output_folder / "processed_treasury_rates.csv"

    # Save processed data
    df.to_csv(output_file)

    print(f"Processed file saved to: {output_file}")

    return df


# Execute function
df_rates = load_and_process_rates(
    r"C:\Users\56946\Documents\financial_pricing_env2\data\raw\daily-treasury-rates.csv"
)

print(df_rates.head())
