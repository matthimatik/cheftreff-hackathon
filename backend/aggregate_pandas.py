import pandas as pd


def aggregate_dataframe(df: pd.DataFrame) -> dict:
    if len(df) < 100:
        n = len(df)
    else:
        n = 100
    sample = df.sample(n=n, random_state=1)
    info = df.info()
    describe = df.describe()
    col_describe = {col: {'describe': df[col].describe(), 'unique': df[col].unique()} for col in df.columns}
    return {
        "sample": sample.to_dict(orient="records"),
        "info": info,
        "describe": repr(describe),
        "col_describe": col_describe.items(),
    }

if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("backend/data/energy_prices.csv")
    result = aggregate_dataframe(df)
    print(result)
