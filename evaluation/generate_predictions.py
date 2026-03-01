import pandas as pd
from retriever.recommender import recommend

test = pd.read_excel("../data/Gen_AI Dataset.xlsx")

rows = []

for _, row in test.iterrows():

    query = row["query"]

    preds = recommend(query, 10)

    for p in preds:

        rows.append({
            "query": query,
            "assessment_url": p["url"]
        })

pd.DataFrame(rows).to_csv("predictions.csv", index=False)

print("predictions.csv generated")