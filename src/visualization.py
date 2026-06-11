import matplotlib.pyplot as plt
import seaborn as sns

def plot_results(df):
    # 1. PCA Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='Cluster', palette='viridis', s=70)
    plt.title('PCA Projection - Customer Segments')
    plt.savefig('outputs/pca_plot.png')
    plt.close()
    
    # 2. Income vs Spending Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Annual Income (₹ Lakhs)', y='Spending_Score', hue='Cluster', palette='tab10', s=70)
    plt.title('Customer Clusters: Income vs Spending')
    plt.savefig('outputs/cluster_plot.png')
    plt.close()
    
    print("✅ Graphs saved in 'outputs/' folder")