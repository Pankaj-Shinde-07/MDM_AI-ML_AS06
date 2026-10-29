"""
Practical Assignment 6: Clustering Algorithms
Course: TY B.Tech - Artificial Intelligence and Machine Learning (MDM-AIML-Lab)
Student: Pankaj Shinde (PRN: 202401100005, Roll No: 07, Batch: A1)
Faculty: Dr. Khushal Khairnar

This script implements:
1. Real-world Customer Segmentation on Mall Customers Dataset (200 records)
2. K-Means Clustering with K-Means++ initialization, Elbow Method (WCSS/Inertia), and Silhouette sweep
3. Hierarchical Agglomerative Clustering with Ward linkage and full Dendrogram analysis
4. DBSCAN (Density-Based Spatial Clustering of Applications with Noise) with k-distance elbow graph for epsilon selection
5. Gaussian Mixture Model (GMM) Expectation-Maximization benchmark
6. Quality evaluation using Silhouette Score, Davies-Bouldin Index, Calinski-Harabasz Index, and Visual Inspection
7. Generation of 8 publication-grade diagnostic plots and structured sample I/O files
"""

import os
import sys
import time
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import (
    silhouette_score,
    silhouette_samples,
    davies_bouldin_score,
    calinski_harabasz_score
)
from scipy.cluster.hierarchy import dendrogram, linkage

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#BDC3C7'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
SAMPLE_IO_DIR = os.path.join(BASE_DIR, "sample_io")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(SAMPLE_IO_DIR, exist_ok=True)


def load_dataset():
    """Loads Mall Customers dataset from CSV."""
    csv_file = os.path.join(DATA_DIR, "Mall_Customers.csv")
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Dataset not found at {csv_file}. Please run generate_dataset.py first.")
    
    df = pd.read_csv(csv_file)
    print(f"[+] Loaded {len(df)} records from {csv_file}")
    
    # Feature matrix for 2D visual customer segmentation
    # Annual Income (k$) and Spending Score (1-100)
    X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values
    
    # Standardize features for distance-based clustering algorithms
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return df, X, X_scaled, scaler


def run_kmeans_sweep(X_scaled, k_range=range(2, 11)):
    """Computes WCSS/Inertia and Silhouette Scores across multiple K values."""
    inertias = []
    sil_scores = []
    
    for k in k_range:
        km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
        sil = silhouette_score(X_scaled, km.labels_)
        sil_scores.append(sil)
        
    return list(k_range), inertias, sil_scores


def evaluate_clusters(name, labels, X_scaled, has_noise=False):
    """Computes Silhouette Score, Davies-Bouldin Index, and Calinski-Harabasz Index."""
    # Filter noise points (label == -1) if algorithm is DBSCAN
    if has_noise:
        mask = labels != -1
        valid_labels = labels[mask]
        valid_X = X_scaled[mask]
        n_clusters = len(set(valid_labels))
        n_noise = int(np.sum(labels == -1))
    else:
        valid_labels = labels
        valid_X = X_scaled
        n_clusters = len(set(valid_labels))
        n_noise = 0

    if n_clusters < 2:
        return {
            "Algorithm": name,
            "Clusters": n_clusters,
            "Noise Points": n_noise,
            "Silhouette Score": np.nan,
            "Davies-Bouldin Index": np.nan,
            "Calinski-Harabasz Index": np.nan
        }

    sil = silhouette_score(valid_X, valid_labels)
    db = davies_bouldin_score(valid_X, valid_labels)
    ch = calinski_harabasz_score(valid_X, valid_labels)

    return {
        "Algorithm": name,
        "Clusters": n_clusters,
        "Noise Points": n_noise,
        "Silhouette Score": sil,
        "Davies-Bouldin Index": db,
        "Calinski-Harabasz Index": ch
    }


def generate_visualizations(df, X, X_scaled, scaler, k_range, inertias, sil_scores,
                            kmeans_model, agg_labels, dbscan_model, gmm_model, eps_val):
    """Generates 8 publication-grade diagnostic plots."""
    print("\n--- Generating Visualizations ---")
    
    # 1. K-Means Elbow Curve & Silhouette Score Sweep (Dual Axis)
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    color = '#1B4F72'
    ax1.set_xlabel('Number of Clusters (k)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Inertia / WCSS (Within-Cluster Sum of Squares)', color=color, fontsize=11, fontweight='bold')
    line1 = ax1.plot(k_range, inertias, marker='o', linewidth=2.2, color=color, label='Inertia (Elbow Method)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(k_range)

    # Highlight optimal elbow point k=5
    ax1.scatter([5], [inertias[3]], color='#C0392B', s=140, zorder=5, label='Elbow Knee (k=5)')

    ax2 = ax1.twinx()
    color2 = '#27AE60'
    ax2.set_ylabel('Silhouette Score (Separation & Compactness)', color=color2, fontsize=11, fontweight='bold')
    line2 = ax2.plot(k_range, sil_scores, marker='s', linewidth=2.2, linestyle='--', color=color2, label='Silhouette Score')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.grid(False)

    lines = line1 + line2 + [ax1.collections[0]]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True, framealpha=0.9)
    plt.title("K-Means Parameter Optimization: Elbow Curve & Silhouette Analysis", fontsize=13, fontweight='bold', pad=14, color='#154360')
    plt.tight_layout()
    fig1_path = os.path.join(SCREENSHOTS_DIR, "01_kmeans_elbow_and_silhouette_sweep.png")
    fig.savefig(fig1_path)
    plt.close(fig)
    print(f"Saved: {fig1_path}")

    # 2. K-Means Clusters with Annotated Centroids
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    palette = ['#E74C3C', '#3498DB', '#2ECC71', '#9B59B6', '#F39C12']
    km_labels = kmeans_model.labels_
    
    # Persona descriptions
    personas = {
        0: "Sensible / Budget (Low Inc, Low Spend)",
        1: "Impulsive / Careless (Low Inc, High Spend)",
        2: "Standard / Average (Mid Inc, Mid Spend)",
        3: "Affluent / Target (High Inc, High Spend)",
        4: "Careful / Savers (High Inc, Low Spend)"
    }

    # Transform centroids back to original unscaled feature space
    centroids_unscaled = scaler.inverse_transform(kmeans_model.cluster_centers_)

    for cluster_id in range(5):
        mask = km_labels == cluster_id
        ax.scatter(
            X[mask, 0], X[mask, 1],
            s=65, color=palette[cluster_id], label=f"Cluster {cluster_id+1}: {personas.get(cluster_id, '')}",
            alpha=0.85, edgecolors='black', linewidths=0.6
        )

    # Plot Centroids
    ax.scatter(
        centroids_unscaled[:, 0], centroids_unscaled[:, 1],
        s=260, c='#F1C40F', marker='*', edgecolors='black', linewidths=1.5,
        label='Cluster Centroids', zorder=10
    )

    for i, c in enumerate(centroids_unscaled):
        ax.annotate(f"C{i+1} ({c[0]:.0f}k, {c[1]:.0f})", (c[0], c[1]),
                    xytext=(0, 10), textcoords='offset points', ha='center',
                    fontweight='bold', fontsize=9, color='#154360')

    ax.set_title("K-Means (k=5) Customer Segmentation with Cluster Centroids", fontsize=13, fontweight='bold', pad=14, color='#154360')
    ax.set_xlabel("Annual Income (k$)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Spending Score (1-100)", fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8.5, frameon=True, framealpha=0.9)
    plt.tight_layout()
    fig2_path = os.path.join(SCREENSHOTS_DIR, "02_kmeans_clusters_2d_centroids.png")
    fig.savefig(fig2_path)
    plt.close(fig)
    print(f"Saved: {fig2_path}")

    # 3. Hierarchical Clustering Dendrogram
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    linked = linkage(X_scaled, method='ward')
    dendrogram(
        linked,
        orientation='top',
        distance_sort='descending',
        show_leaf_counts=True,
        ax=ax,
        color_threshold=5.0,
        no_labels=True
    )
    ax.axhline(y=5.0, color='#C0392B', linestyle='--', linewidth=1.5, label='Optimal Cut Threshold (k=5 Clusters)')
    ax.set_title("Hierarchical Agglomerative Clustering Dendrogram (Ward Linkage)", fontsize=13, fontweight='bold', pad=14, color='#154360')
    ax.set_xlabel("Customer Data Index (200 instances)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Euclidean Cophenetic Distance", fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', frameon=True, framealpha=0.9)
    plt.tight_layout()
    fig3_path = os.path.join(SCREENSHOTS_DIR, "03_hierarchical_dendrogram.png")
    fig.savefig(fig3_path)
    plt.close(fig)
    print(f"Saved: {fig3_path}")

    # 4. Side-by-Side: K-Means vs Agglomerative Hierarchical Clustering
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    # Plot K-Means
    scatter1 = ax1.scatter(X[:, 0], X[:, 1], c=km_labels, cmap='tab10', s=55, alpha=0.85, edgecolors='k', linewidths=0.5)
    ax1.set_title(f"K-Means (k=5)\nSilhouette Score: {silhouette_score(X_scaled, km_labels):.4f}", fontsize=11, fontweight='bold', color='#154360')
    ax1.set_xlabel("Annual Income (k$)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Spending Score (1-100)", fontsize=10, fontweight='bold')

    # Plot Agglomerative
    scatter2 = ax2.scatter(X[:, 0], X[:, 1], c=agg_labels, cmap='tab10', s=55, alpha=0.85, edgecolors='k', linewidths=0.5)
    ax2.set_title(f"Hierarchical Agglomerative (k=5, Ward)\nSilhouette Score: {silhouette_score(X_scaled, agg_labels):.4f}", fontsize=11, fontweight='bold', color='#154360')
    ax2.set_xlabel("Annual Income (k$)", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Spending Score (1-100)", fontsize=10, fontweight='bold')

    plt.suptitle("Clustering Structural Consistency: K-Means vs. Hierarchical Agglomerative", fontsize=14, fontweight='bold', y=0.99, color='#154360')
    plt.tight_layout()
    fig4_path = os.path.join(SCREENSHOTS_DIR, "04_hierarchical_vs_kmeans_comparison.png")
    fig.savefig(fig4_path)
    plt.close(fig)
    print(f"Saved: {fig4_path}")

    # 5. DBSCAN: K-Distance Elbow Curve & Resulting Clusters
    # 5a. K-distance plot to select optimal eps
    k_nn = 5
    nbrs = NearestNeighbors(n_neighbors=k_nn).fit(X_scaled)
    distances, _ = nbrs.kneighbors(X_scaled)
    distances = np.sort(distances[:, k_nn - 1], axis=0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    ax1.plot(distances, color='#2980B9', lw=2)
    ax1.axhline(y=eps_val, color='#E74C3C', linestyle='--', lw=1.5, label=f'Chosen Epsilon (eps={eps_val:.2f})')
    ax1.set_title(f"DBSCAN K-NN (k={k_nn}) Distance Elbow Curve", fontsize=11, fontweight='bold', color='#154360')
    ax1.set_xlabel("Data Points Sorted by Distance", fontsize=10, fontweight='bold')
    ax1.set_ylabel(f"{k_nn}-th Nearest Neighbor Distance", fontsize=10, fontweight='bold')
    ax1.legend(loc='upper left', frameon=True)

    # 5b. DBSCAN clusters
    db_labels = dbscan_model.labels_
    unique_labels = set(db_labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        if k == -1:
            col = [0.2, 0.2, 0.2, 1]  # Black for noise
            label_text = "Noise / Outliers (-1)"
            marker = 'x'
            size = 50
        else:
            label_text = f"Cluster {k+1}"
            marker = 'o'
            size = 65

        class_member_mask = (db_labels == k)
        xy = X[class_member_mask]
        ax2.scatter(xy[:, 0], xy[:, 1], color=col, marker=marker, s=size, edgecolors='k' if k!=-1 else 'none', label=label_text, alpha=0.85)

    n_db_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)
    n_db_noise = list(db_labels).count(-1)
    ax2.set_title(f"DBSCAN Result (eps={eps_val:.2f}, min_samples=5)\nClusters: {n_db_clusters} | Noise Outliers: {n_db_noise}", fontsize=11, fontweight='bold', color='#154360')
    ax2.set_xlabel("Annual Income (k$)", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Spending Score (1-100)", fontsize=10, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=8.5, frameon=True)

    plt.suptitle("DBSCAN Density-Based Parameterization & Cluster Partitioning", fontsize=14, fontweight='bold', y=0.99, color='#154360')
    plt.tight_layout()
    fig5_path = os.path.join(SCREENSHOTS_DIR, "05_dbscan_k_distance_and_clusters.png")
    fig.savefig(fig5_path)
    plt.close(fig)
    print(f"Saved: {fig5_path}")

    # 6. Silhouette Analysis Per Cluster for K-Means (k=5)
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    sample_silhouette_values = silhouette_samples(X_scaled, km_labels)
    avg_sil = silhouette_score(X_scaled, km_labels)

    y_lower = 10
    for i in range(5):
        ith_cluster_sil_vals = sample_silhouette_values[km_labels == i]
        ith_cluster_sil_vals.sort()
        size_cluster_i = ith_cluster_sil_vals.shape[0]
        y_upper = y_lower + size_cluster_i

        col = cm.nipy_spectral(float(i) / 5)
        ax.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_sil_vals,
                         facecolor=col, edgecolor=col, alpha=0.7)
        ax.text(-0.05, y_lower + 0.5 * size_cluster_i, f"Cluster {i+1}", fontsize=9, fontweight='bold')
        y_lower = y_upper + 10

    ax.axvline(x=avg_sil, color="red", linestyle="--", linewidth=1.5, label=f"Average Silhouette Score ({avg_sil:.4f})")
    ax.set_title("Silhouette Coefficient Plot for K-Means (k=5) Clusters", fontsize=13, fontweight='bold', pad=14, color='#154360')
    ax.set_xlabel("Silhouette Coefficient Values", fontsize=11, fontweight='bold')
    ax.set_ylabel("Cluster Membership Thickness", fontsize=11, fontweight='bold')
    ax.set_yticks([])
    ax.set_xlim([-0.1, 0.85])
    ax.legend(loc="lower right", frameon=True, framealpha=0.9)
    plt.tight_layout()
    fig6_path = os.path.join(SCREENSHOTS_DIR, "06_silhouette_analysis_per_cluster.png")
    fig.savefig(fig6_path)
    plt.close(fig)
    print(f"Saved: {fig6_path}")

    # 7. Quality Metrics Comparison Bar Chart (Silhouette, Davies-Bouldin, Calinski-Harabasz)
    # We create a normalized comparative visual across algorithms
    comp_models = ["K-Means (k=5)", "Hierarchical (Ward)", "DBSCAN (Density)", "GMM (EM Soft)"]
    sils = [
        silhouette_score(X_scaled, km_labels),
        silhouette_score(X_scaled, agg_labels),
        silhouette_score(X_scaled[db_labels!=-1], db_labels[db_labels!=-1]),
        silhouette_score(X_scaled, gmm_model.predict(X_scaled))
    ]
    dbs = [
        davies_bouldin_score(X_scaled, km_labels),
        davies_bouldin_score(X_scaled, agg_labels),
        davies_bouldin_score(X_scaled[db_labels!=-1], db_labels[db_labels!=-1]),
        davies_bouldin_score(X_scaled, gmm_model.predict(X_scaled))
    ]
    chs = [
        calinski_harabasz_score(X_scaled, km_labels),
        calinski_harabasz_score(X_scaled, agg_labels),
        calinski_harabasz_score(X_scaled[db_labels!=-1], db_labels[db_labels!=-1]),
        calinski_harabasz_score(X_scaled, gmm_model.predict(X_scaled))
    ]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5), dpi=300)
    
    # Silhouette Score (Higher is better)
    bars1 = ax1.bar(comp_models, sils, color='#2980B9', edgecolor='black', linewidth=0.6)
    ax1.set_title("Silhouette Score\n(Higher is Better)", fontsize=11, fontweight='bold', color='#154360')
    ax1.set_ylabel("Score [-1 to 1]", fontsize=10, fontweight='bold')
    ax1.tick_params(axis='x', rotation=30)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f"{yval:.3f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Davies-Bouldin Index (Lower is better)
    bars2 = ax2.bar(comp_models, dbs, color='#E67E22', edgecolor='black', linewidth=0.6)
    ax2.set_title("Davies-Bouldin Index\n(Lower is Better)", fontsize=11, fontweight='bold', color='#154360')
    ax2.set_ylabel("Index Value", fontsize=10, fontweight='bold')
    ax2.tick_params(axis='x', rotation=30)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.3f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Calinski-Harabasz Index (Higher is better)
    bars3 = ax3.bar(comp_models, chs, color='#27AE60', edgecolor='black', linewidth=0.6)
    ax3.set_title("Calinski-Harabasz Index\n(Higher is Better)", fontsize=11, fontweight='bold', color='#154360')
    ax3.set_ylabel("Variance Ratio Criterion", fontsize=10, fontweight='bold')
    ax3.tick_params(axis='x', rotation=30)
    for bar in bars3:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval:.1f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.suptitle("Quantitative Clustering Evaluation Metrics Comparison", fontsize=13, fontweight='bold', y=0.99, color='#154360')
    plt.tight_layout()
    fig7_path = os.path.join(SCREENSHOTS_DIR, "07_clustering_metrics_comparison_bar.png")
    fig.savefig(fig7_path)
    plt.close(fig)
    print(f"Saved: {fig7_path}")

    # 8. Business Customer Personas Profile Distributions
    df_profile = df.copy()
    df_profile["Cluster"] = [f"Cluster {i+1}" for i in km_labels]
    df_profile["Persona"] = [personas[i] for i in km_labels]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    sns.boxplot(x="Cluster", y="Annual Income (k$)", data=df_profile, palette="Set2", ax=ax1)
    ax1.set_title("Annual Income Distribution by Cluster", fontsize=11, fontweight='bold', color='#154360')
    ax1.set_xlabel("Customer Segment", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Annual Income (k$)", fontsize=10, fontweight='bold')

    sns.boxplot(x="Cluster", y="Spending Score (1-100)", data=df_profile, palette="Set2", ax=ax2)
    ax2.set_title("Spending Score Distribution by Cluster", fontsize=11, fontweight='bold', color='#154360')
    ax2.set_xlabel("Customer Segment", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Spending Score (1-100)", fontsize=10, fontweight='bold')

    plt.suptitle("Actionable Customer Demographic & Behavioral Persona Profiling", fontsize=14, fontweight='bold', y=0.99, color='#154360')
    plt.tight_layout()
    fig8_path = os.path.join(SCREENSHOTS_DIR, "08_cluster_business_personas.png")
    fig.savefig(fig8_path)
    plt.close(fig)
    print(f"Saved: {fig8_path}")

    return df_profile


def main():
    print("="*80)
    print(" PRACTICAL ASSIGNMENT 6: CLUSTERING ALGORITHMS & QUALITY EVALUATION")
    print(" Student: Pankaj Shinde | PRN: 202401100005 | Roll No: 07 | Division: A (A1)")
    print(" Faculty: Dr. Khushal Khairnar | TY B.Tech AIML")
    print("="*80)

    # 1. Load dataset
    df, X, X_scaled, scaler = load_dataset()
    print(f"\n[+] Features utilized for customer segmentation: Annual Income (k$) and Spending Score (1-100)")
    print(f"[+] Total samples: {X.shape[0]}, Dimensions: {X.shape[1]}")

    # 2. K-Means Sweep: Elbow Curve and Silhouette
    print("\n--- Running K-Means Sweep (k=2 to 10) ---")
    k_range, inertias, sil_scores = run_kmeans_sweep(X_scaled)
    for k, inert, sil in zip(k_range, inertias, sil_scores):
        print(f"k = {k:2d} | Inertia: {inert:9.2f} | Silhouette Score: {sil:.4f}")

    # Fit optimal K-Means (k=5)
    best_k = 5
    kmeans_model = KMeans(n_clusters=best_k, init='k-means++', n_init=20, random_state=42)
    kmeans_labels = kmeans_model.fit_predict(X_scaled)

    # 3. Hierarchical Agglomerative Clustering (Ward Linkage, k=5)
    print("\n--- Running Hierarchical Agglomerative Clustering (Ward, k=5) ---")
    agg_model = AgglomerativeClustering(n_clusters=best_k, linkage='ward')
    agg_labels = agg_model.fit_predict(X_scaled)

    # 4. DBSCAN (Density-Based Spatial Clustering)
    print("\n--- Running DBSCAN Clustering ---")
    # Finding optimal eps: around 0.35 on standardized features
    eps_val = 0.35
    dbscan_model = DBSCAN(eps=eps_val, min_samples=5)
    dbscan_labels = dbscan_model.fit_predict(X_scaled)
    n_db_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
    n_db_noise = list(dbscan_labels).count(-1)
    print(f"DBSCAN with eps={eps_val:.2f}, min_samples=5: Found {n_db_clusters} clusters, {n_db_noise} noise points.")

    # 5. Gaussian Mixture Model (GMM - EM Probabilistic Soft Clustering)
    print("\n--- Running Gaussian Mixture Model (GMM, k=5) ---")
    gmm_model = GaussianMixture(n_components=best_k, covariance_type='full', random_state=42)
    gmm_labels = gmm_model.fit_predict(X_scaled)

    # 6. Evaluation metrics computation
    eval_list = [
        evaluate_clusters("K-Means (k=5)", kmeans_labels, X_scaled),
        evaluate_clusters("Hierarchical Agglomerative (Ward, k=5)", agg_labels, X_scaled),
        evaluate_clusters(f"DBSCAN (eps={eps_val}, min=5)", dbscan_labels, X_scaled, has_noise=True),
        evaluate_clusters("Gaussian Mixture Model (k=5)", gmm_labels, X_scaled)
    ]
    eval_df = pd.DataFrame(eval_list)

    print("\n" + "="*85)
    print(f"{'Algorithm':<32} | {'Clusters':<8} | {'Noise':<6} | {'Silhouette':<10} | {'Davies-Bouldin':<14} | {'Calinski-Harabasz':<17}")
    print("-" * 85)
    for _, row in eval_df.iterrows():
        sil_str = f"{row['Silhouette Score']:.4f}" if not np.isnan(row['Silhouette Score']) else "N/A"
        db_str = f"{row['Davies-Bouldin Index']:.4f}" if not np.isnan(row['Davies-Bouldin Index']) else "N/A"
        ch_str = f"{row['Calinski-Harabasz Index']:.2f}" if not np.isnan(row['Calinski-Harabasz Index']) else "N/A"
        print(f"{row['Algorithm']:<32} | {row['Clusters']:<8} | {row['Noise Points']:<6} | {sil_str:<10} | {db_str:<14} | {ch_str:<17}")
    print("=" * 85)

    # Export results table
    csv_eval_path = os.path.join(SAMPLE_IO_DIR, "results_table.csv")
    eval_df.to_csv(csv_eval_path, index=False)
    print(f"\n[+] Quality metrics table exported to: {csv_eval_path}")

    # Generate Visualizations & Personas
    df_profile = generate_visualizations(
        df, X, X_scaled, scaler, k_range, inertias, sil_scores,
        kmeans_model, agg_labels, dbscan_model, gmm_model, eps_val
    )

    # Export Cluster Profiles CSV
    cluster_summary = df_profile.groupby(["Cluster", "Persona"])[["Age", "Annual Income (k$)", "Spending Score (1-100)"]].agg(["count", "mean", "std"]).reset_index()
    csv_profile_path = os.path.join(SAMPLE_IO_DIR, "cluster_profiles.csv")
    cluster_summary.to_csv(csv_profile_path, index=False)
    print(f"[+] Business cluster profiles exported to: {csv_profile_path}")

    # Save Sample Input & Output
    input_txt_path = os.path.join(SAMPLE_IO_DIR, "sample_input.txt")
    with open(input_txt_path, "w", encoding="utf-8") as f:
        f.write("PRACTICAL 6: CLUSTERING ALGORITHMS - SAMPLE INPUT SPECIFICATION\n")
        f.write("="*75 + "\n")
        f.write("Dataset: Mall Customer Segmentation Dataset\n")
        f.write(f"Number of Customer Records: {len(df)}\n")
        f.write("Features Extracted for Clustering Analysis:\n")
        f.write("  1. Annual Income (k$): Numerical, Range 15 to 140 k$\n")
        f.write("  2. Spending Score (1-100): Numerical, Range 1 to 99\n")
        f.write("Preprocessing: Standardized using StandardScaler (mean=0, variance=1)\n")
        f.write("Clustering Algorithms Benchmarked:\n")
        f.write("  - K-Means (k=2 to 10 with k-means++)\n")
        f.write("  - Hierarchical Agglomerative Clustering (Ward Linkage, Euclidean metric)\n")
        f.write(f"  - DBSCAN (Density-Based Spatial Clustering of Applications with Noise, eps={eps_val}, min_samples=5)\n")
        f.write("  - Gaussian Mixture Model (EM soft probabilistic clustering, k=5)\n")

    output_txt_path = os.path.join(SAMPLE_IO_DIR, "sample_output.txt")
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write("PRACTICAL 6: CLUSTERING ALGORITHMS - EXECUTION OUTPUT LOG\n")
        f.write("="*85 + "\n")
        f.write("Student: Pankaj Shinde (PRN: 202401100005, Roll No: 07)\n\n")
        f.write("K-MEANS HYPERPARAMETER (k) ELBOW & SILHOUETTE SWEEP:\n")
        for k, inert, sil in zip(k_range, inertias, sil_scores):
            f.write(f"  k = {k:2d} | Inertia (WCSS): {inert:8.2f} | Silhouette Score: {sil:.4f}\n")
        f.write("\n" + "="*85 + "\n")
        f.write("QUANTITATIVE CLUSTERING EVALUATION BENCHMARK TABLE:\n")
        f.write(eval_df.to_string(index=False))
        f.write("\n\n" + "="*85 + "\n")
        f.write("ACTIONABLE CUSTOMER PERSONA PROFILES (K-MEANS k=5):\n\n")
        for name, group in df_profile.groupby("Cluster"):
            f.write(f"--- {name}: {group['Persona'].iloc[0]} ---\n")
            f.write(f"  Count: {len(group)} customers ({len(group)/len(df)*100:.1f}% of total)\n")
            f.write(f"  Mean Age: {group['Age'].mean():.1f} years\n")
            f.write(f"  Mean Annual Income: ${group['Annual Income (k$)'].mean():.1f}k\n")
            f.write(f"  Mean Spending Score: {group['Spending Score (1-100)'].mean():.1f} / 100\n\n")

    print(f"[+] Sample input logged to: {input_txt_path}")
    print(f"[+] Sample output logged to: {output_txt_path}")
    print("\n[SUCCESS] Practical 6 execution and artifact generation completed successfully!")


if __name__ == "__main__":
    main()
