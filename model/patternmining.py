import pickle
import os
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

file_path = os.getenv("DATASET")
df = pd.read_csv(file_path)

grouped_tracks = df.groupby('pid')['track_name'].apply(set)

def encode_tracks_to_binary(tracks):
    return pd.Series(1, index=tracks)

onehot_data = grouped_tracks.apply(encode_tracks_to_binary).fillna(0).astype(bool)

frequent_itemsets = fpgrowth(onehot_data, min_support=0.1, use_colnames=True)

rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.15)
rules = rules[['antecedents', 'consequents', 'antecedent support', 'consequent support', 'confidence']]
rules = rules.sort_values(by=["confidence"], ascending=False)

rules_pickle_path = "/pickle/rules.pkl"
with open(rules_pickle_path, "wb") as f:
    pickle.dump(rules, f)

print(f"Rules successfully saved to {rules_pickle_path}")