import pandas as pd

def query_assistant(question, logs_file="logs.csv"):
    try:
        df = pd.read_csv(logs_file)
    except FileNotFoundError:
        return "No detection logs available yet."

    if "how many" in question.lower() and "person" in question.lower():
        count = df[df["object"] == "person"].shape[0]
        return f"{count} persons detected so far."

    elif "average confidence" in question.lower():
        avg_conf = df["confidence"].mean()
        return f"Average confidence: {avg_conf:.2f}"

    elif "objects" in question.lower():
        objects = df["object"].unique()
        return f"Objects detected: {', '.join(objects)}"

    else:
        return "Sorry, I can’t answer that question yet."
