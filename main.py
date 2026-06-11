from src.data_prep import prepare_data
from src.segmentation import perform_segmentation
from src.visualization import plot_results
import os

def main():
    print("🚀 Starting Market & Customer Segmentation Analysis...")
    
    # Path to your raw Kaggle file
    raw_data_path = 'data/mall_customers_india.csv' 
    
    if not os.path.exists(raw_data_path):
        print(f"❌ Error: {raw_data_path} not found! Please add the file.")
        return

    # 1. Prepare Data
    processed_path = prepare_data(raw_data_path)
    
    # 2. Run Segmentation
    df_segmented, summary = perform_segmentation(processed_path)
    
    # 3. Generate Visuals
    plot_results(df_segmented)
    
    # 4. Final Table Output (Screenshot lo unnattu)
    print("\n📊 Segment Summary (Average Values):")
    print(summary)
    print("\n✨ All files generated successfully in 'outputs/' folder!")

if __name__ == "__main__":
    main()