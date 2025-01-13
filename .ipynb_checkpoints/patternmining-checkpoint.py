import pickle
import os
import subprocess
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

file_path = 'data/2023_spotify_ds1.csv'
df = pd.read_csv(file_path)

# Step 2: Group by 'pid' and create a transaction list of tracks
# Grouping by pid and aggregating the track names
grouped_tracks = df.groupby('pid')['track_name'].apply(set)
#grouped_tracks = df.groupby('pid')['track_uri'].apply(set)

# Step 3: Convert the grouped data into a boolean matrix suitable for FP-Growth
# Use a function to encode each playlist as binary (1 for tracks present, 0 for not)
def encode_tracks_to_binary(tracks):
    return pd.Series(1, index=tracks)

onehot_data = grouped_tracks.apply(encode_tracks_to_binary).fillna(0).astype(bool)

# Step 4: Apply FP-Growth algorithm
frequent_itemsets = fpgrowth(onehot_data, min_support=0.15, use_colnames=True)

# Step 5: Generate association rules from the frequent itemsets
rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.15)
rules = rules[['antecedents', 'consequents', 'antecedent support', 'consequent support', 'confidence']]
rules = rules.sort_values(by=["confidence"], ascending=False)

with open('/pickle/rules.pkl', 'wb') as f:
    pickle.dump(rules, f)

with open('/pickle/date.pkl', 'wb') as f:
    pickle.dump(date.today(), f)

subprocess.run(["ls", "-l", "/pickle"])
