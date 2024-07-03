import pandas as pd

def post_process_csv(input_path: str, output_path: str = None):
    if output_path is None:
        output_path = input_path
    df = pd.read_csv(input_path)
    df["name"] = df["name"].str.replace("a black and white ", "")
    df["name"] = df["name"].str.replace("a cartoon character", "a character")
    df.to_csv(output_path)
