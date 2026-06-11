import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

def perform_segmentation(data_path):
    df = pd.read_csv(data_path)
    os.makedirs('outputs', exist_ok=True)
    
    # Clustering ki kavalsina features
    features = ['Age', 'Annual Income (₹ Lakhs)', 'Spending_Score', 'Frequency', 'Monetary']
    X = df[features]
    
    # 1. Scaling (Data ni okate range loki teevali)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. ELBOW METHOD (Finding Optimal K)
    print("📉 Calculating Elbow Method...")
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
        kmeans.fit(X_scaled)
        wcss.append(kmeans.inertia_)
    
    # Elbow Graph Save Cheydam
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 11), wcss, marker='o', linestyle='--', color='red')
    plt.title('Elbow Method (Finding Best Number of Clusters)')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('WCSS (Error)')
    plt.grid(True)
    plt.savefig('outputs/elbow_plot.png') # Saving to outputs
    plt.close()
    print("✅ Elbow Plot saved in 'outputs/elbow_plot.png'")

    # 3. K-MEANS (Final Clustering with k=5)
    kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # 4. PCA (Dimensionality Reduction for 2D Plot)
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(X_scaled)
    df['PCA1'] = pca_data[:, 0]
    df['PCA2'] = pca_data[:, 1]
    
    # Save Results
    df.to_csv('outputs/customer_segments.csv', index=False)
    
    # Summary Table
    summary = df.groupby('Cluster')[features].mean().round(2)
    summary.to_csv('outputs/segment_summary.csv')
    
    return df, summary