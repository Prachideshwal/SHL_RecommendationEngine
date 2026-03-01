import pandas as pd
from retriever.recommender import recommend

test = pd.read_excel("../data/Gen_AI Dataset.xlsx")

recall = []

for _, row in test.iterrows():

    query = row["query"]

    true_urls = set(row["assessment_url"].split(","))

    preds = recommend(query, 10)

    pred_urls = set([p["url"] for p in preds])

    hit = len(true_urls.intersection(pred_urls))

    recall.append(hit / len(true_urls))

print("Mean Recall@10:", sum(recall)/len(recall))