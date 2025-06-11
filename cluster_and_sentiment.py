import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from transformers import pipeline

# Load dataset
csv_path = 'prepared.csv'
df = pd.read_csv(csv_path)

# Select numeric columns for clustering (Likert scale responses)
# Columns 5 through 49 are Likert numeric columns
likert_cols = df.columns[5:50]
X = df[likert_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

# Standardize and cluster
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# Sentiment analysis on free-text column using IndoBERT
text_col = df.columns[50]
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="w11wo/indonesian-roberta-base-sentiment-classifier",
)

label_to_score = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}

def get_polarity(text: str) -> float:
    if pd.isna(text) or not str(text).strip():
        return 0.0
    result = sentiment_pipeline(str(text))[0]
    label = result.get("label", "neutral").lower()
    score = result.get("score", 0.0)
    return score * label_to_score.get(label, 0.0)

# Add sentiment polarity
df['sentiment'] = df[text_col].apply(get_polarity)

# Output some basic information
cluster_counts = df['cluster'].value_counts().sort_index()
print('Cluster counts:')
print(cluster_counts)
print('\nSentiment polarity summary:')
print(df['sentiment'].describe())

# Save results
output_csv = 'cluster_sentiment_output.csv'
df.to_csv(output_csv, index=False)
print(f"Results written to {output_csv}")

