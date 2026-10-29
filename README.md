# Practical 6 – Clustering Algorithms & Quality Evaluation

**TY B.Tech. – Artificial Intelligence and Machine Learning**  
**Course Code:** MDM-AIML-Lab (Unit: Unsupervised Learning / Cluster Analysis)

| Field | Details |
|---|---|
| **Student Name** | Pankaj Shinde |
| **PRN** | 202401100005 |
| **Branch** | Software Engineering |
| **Division / Batch** | A / A1 |
| **Roll No.** | 07 |
| **Faculty In-Charge** | Dr. Khushal Khairnar |
| **Academic Term** | Semester V / A.Y. 2026–2027 |
| **Date of Submission** | 28-10-2026 |

---

## 1. Problem Statement

Implement clustering algorithms on a real-world dataset to identify meaningful groups within the data. Evaluate the quality of clustering results using appropriate metrics such as **Silhouette Score**, **Davies-Bouldin Index**, **Calinski-Harabasz Index**, and **Visual Inspection** across distinct clustering paradigms (**Centroid-based K-Means**, **Connectivity-based Hierarchical Agglomerative**, and **Density-based DBSCAN**).

---

## 2. Algorithms & Mathematical Principles

| Algorithm | Clustering Paradigm | Mathematical Principle / Objective Function | Key Hyperparameters |
|---|---|---|---|
| **K-Means Clustering** | Partitioning / Centroid-Based | Minimizes Within-Cluster Sum of Squares (Inertia / WCSS):<br>$J = \sum_{k=1}^K \sum_{x_i \in C_k} \|\|x_i - \mu_k\|\|^2$<br>Uses **K-Means++** smart probabilistic seeding ($D(x)^2$ sampling) to accelerate convergence and eliminate local minima traps. | `n_clusters=5`, `init='k-means++'`, `n_init=20`, `max_iter=300` |
| **Hierarchical Agglomerative** | Connectivity / Bottom-up Tree | Bottom-up greedy agglomeration starting with $N$ singleton clusters. Minimizes variance increase at each step using **Ward's Minimum Variance Criterion**:<br>$\Delta ESS_{A,B} = \frac{n_A n_B}{n_A + n_B} \|\mu_A - \mu_B\|^2$ | `n_clusters=5`, `linkage='ward'`, `metric='euclidean'` |
| **DBSCAN** | Density-Based Spatial | Identifies dense continuous manifolds separated by low-density regions. Classifies points as Core ($|N_\epsilon(p)| \ge \text{MinPts}$), Border, or Noise Outliers.<br>Robust to arbitrary non-spherical shapes. | `eps=0.35`, `min_samples=5`, `metric='euclidean'` |
| **Gaussian Mixture Model (GMM)** | Distribution / Probabilistic Soft | Models data distribution as a convex mixture of $K$ multivariate Gaussian components $\mathcal{N}(\mu_k, \Sigma_k)$ via the **Expectation-Maximization (EM)** algorithm to maximize log-likelihood. | `n_components=5`, `covariance_type='full'`, `random_state=42` |

---

## 3. Real-World Dataset: Mall Customer Segmentation

The study benchmarks the canonical **Mall Customer Segmentation Dataset** representing real-world commercial consumer transactions:
- **Total Records:** 200 customer profiles
- **Features Extracted:**
  - `Annual Income (k$)`: Customer annual earnings in thousands of USD (Range: \$15k to \$140k).
  - `Spending Score (1-100)`: Behavioral index computed by the mall based on purchase frequency, basket value, and loyalty interactions (Range: 1 to 99).
- **Preprocessing:** Features are standardized using `StandardScaler` ($z = \frac{x - \mu}{\sigma}$) to place income and spending scores on equivalent unit-variance Euclidean footing.

---

## 4. Repository Structure

```
MDM_AI-ML_AS06/
├── clustering_algorithms.py       # Main Python executable script
├── requirements.txt               # Dependencies (scikit-learn, scipy, pandas, matplotlib, seaborn)
├── README.md                      # Comprehensive project documentation
├── data/
│   └── Mall_Customers.csv         # Benchmark 200-sample customer dataset
├── sample_io/
│   ├── sample_input.txt           # Detailed dataset and parameter specification
│   ├── sample_output.txt          # Complete execution logs and reports
│   ├── results_table.csv          # Structured evaluation metrics in CSV format
│   └── cluster_profiles.csv       # Actionable business persona profile table
└── screenshots/
    ├── 01_kmeans_elbow_and_silhouette_sweep.png   # Dual-axis Elbow curve (WCSS) & Silhouette sweep
    ├── 02_kmeans_clusters_2d_centroids.png        # K-Means clusters with annotated centroids
    ├── 03_hierarchical_dendrogram.png             # Ward linkage dendrogram with optimal cut line
    ├── 04_hierarchical_vs_kmeans_comparison.png   # Side-by-side scatter comparison (K-Means vs Agg)
    ├── 05_dbscan_k_distance_and_clusters.png      # K-NN distance plot and DBSCAN clusters with noise
    ├── 06_silhouette_analysis_per_cluster.png     # Silhouette coefficient plot for individual samples
    ├── 07_clustering_metrics_comparison_bar.png   # Quantitative evaluation comparison bar charts
    └── 08_cluster_business_personas.png           # Demographic & behavioral boxplots per segment
```

---

## 5. Quantitative Clustering Evaluation Metrics

The clustering models were evaluated across three foundational unsupervised quality indices:

| Clustering Algorithm | Paradigm | Clusters ($K$) | Noise Points | Silhouette Score $\uparrow$ | Davies-Bouldin Index $\downarrow$ | Calinski-Harabasz Index $\uparrow$ |
|---|---|---|---|---|---|---|
| **DBSCAN ($\epsilon=0.35, \text{MinPts}=5$)** | Density | 5 | 27 | **0.6347** | **0.4359** | **354.50** |
| **K-Means ($k=5$, k-means++)** | Centroid | 5 | 0 | **0.5844** | **0.5126** | **315.69** |
| **Gaussian Mixture Model (k=5)** | Probabilistic | 5 | 0 | 0.5834 | 0.5104 | 307.78 |
| **Hierarchical Agglomerative (Ward)** | Connectivity | 5 | 0 | 0.5748 | 0.5214 | 301.95 |

### Metric Formulations & Mathematical Meaning:
1. **Silhouette Score ($s \in [-1, +1]$):**  
   $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$  
   Where $a(i)$ is mean intra-cluster distance and $b(i)$ is mean nearest-cluster distance. Higher values indicate tight, well-separated clusters.
2. **Davies-Bouldin Index ($DB \ge 0$):**  
   $$DB = \frac{1}{K}\sum_{i=1}^K \max_{j \neq i} \left( \frac{\sigma_i + \sigma_j}{d(c_i, c_j)} \right)$$  
   Measures the maximum ratio of cluster scatter to centroid separation. Lower values indicate superior compactness and separation.
3. **Calinski-Harabasz Index (Variance Ratio Criterion):**  
   $$CH = \frac{\text{Tr}(B_K) / (K - 1)}{\text{Tr}(W_K) / (N - K)}$$  
   Ratio of between-cluster dispersion to within-cluster dispersion. Higher values indicate dense, well-isolated clusters.

---

## 6. Actionable Customer Persona Segmentation

Through K-Means and Hierarchical Clustering, five distinct behavioral consumer segments were uncovered:

| Cluster ID | Segment Persona | Customer Share | Mean Annual Income | Mean Spending Score | Marketing & Business Strategy |
|---|---|---|---|---|---|
| **Cluster 1** | **Sensible / Budget Consumers** | 23 customers (11.5%) | \$26.3k (Low) | 20.9 / 100 (Low) | Discount campaigns, budget-friendly loyalty promotions, value-oriented messaging. |
| **Cluster 2** | **Careless / Impulsive Shoppers** | 22 customers (11.0%) | \$25.7k (Low) | 79.4 / 100 (High) | Flash sales, trend-driven youth marketing, gamified discounts, installment payment options. |
| **Cluster 3** | **Standard / Moderate Consumers** | 81 customers (40.5%) | \$55.3k (Mid) | 49.5 / 100 (Mid) | Reliable middle-class retail; seasonal offers, family bundle packages. |
| **Cluster 4** | **Affluent / Target Customers (VIP)** | 39 customers (19.5%) | \$86.5k (High) | 82.1 / 100 (High) | **Primary Target:** Premium concierge services, luxury brand previews, VIP events. |
| **Cluster 5** | **Careful / Frugal Savers** | 35 customers (17.5%) | \$88.2k (High) | 17.1 / 100 (Low) | Wealth management, long-term premium quality warranties, high-value investment appeals. |

---

## 7. Visual Inspection & Diagnostic Plots Summary

1. **Elbow Curve & Silhouette Sweep (`01_kmeans_elbow_and_silhouette_sweep.png`):** Confirms an unmistakable inflection elbow at $K=5$, where WCSS drops from 258.70 to 53.51 and Silhouette reaches its global peak of **0.5844**.
2. **Centroid Localization (`02_kmeans_clusters_2d_centroids.png`):** Displays clearly bounded clusters with yellow star centroids accurately anchoring each of the five commercial segments.
3. **Ward Linkage Dendrogram (`03_hierarchical_dendrogram.png`):** Shows natural hierarchical clustering with large vertical distance gaps confirming that five clusters form the natural structure.
4. **K-Means vs. Agglomerative Comparison (`04_hierarchical_vs_kmeans_comparison.png`):** Demonstrates complete geometric consistency between centroid partitioning and agglomerative tree merging.
5. **DBSCAN Density Structure (`05_dbscan_k_distance_and_clusters.png`):** The 5-NN distance elbow clearly reveals $\epsilon=0.35$ as the knee, effectively identifying core dense cluster centers while isolating 27 peripheral boundary points as outliers.
6. **Silhouette Analysis (`06_silhouette_analysis_per_cluster.png`):** Validates that all five clusters have samples exceeding the average silhouette threshold of 0.5844 with minimal negative coefficients, proving absence of artificial cluster fragmentation.
7. **Quality Metrics Comparison (`07_clustering_metrics_comparison_bar.png`):** Quantitative visualization contrasting Silhouette, Davies-Bouldin, and Calinski-Harabasz across the four algorithms.
8. **Persona Demographics Profiling (`08_cluster_business_personas.png`):** Boxplot distributions confirming clear separation of income and spending across customer segments.

---

## 8. Comparative Analysis: When to Use Each Clustering Algorithm

```
                                CLUSTERING PARADIGM COMPARISON
┌──────────────────────┬──────────────────────┬────────────────────────┬────────────────────────┐
│ Algorithm            │ Cluster Geometry     │ Ideal Use Case         │ Critical Limitations   │
├──────────────────────┼──────────────────────┼────────────────────────┼────────────────────────┤
│ K-Means++            │ Convex, spherical,   │ Fast large-scale       │ Requires pre-defined   │
│                      │ equal variance       │ customer segmentation; │ K; sensitive to non-   │
│                      │                      │ clean tabular data     │ spherical outliers     │
├──────────────────────┼──────────────────────┼────────────────────────┼────────────────────────┤
│ Hierarchical         │ Arbitrary tree       │ Biological taxonomies; │ $O(N^2)$ memory &      │
│ Agglomerative        │ hierarchies; nested  │ small-to-medium        │ $O(N^3)$ compute;      │
│ (Ward)               │ sub-clusters         │ datasets where tree    │ irreversible merges    │
│                      │                      │ visualization is key   │                        │
├──────────────────────┼──────────────────────┼────────────────────────┼────────────────────────┤
│ DBSCAN               │ Arbitrary non-linear │ Spatial geo-data; GPS  │ Fails on datasets with │
│                      │ manifolds, density-  │ tracking; anomaly &    │ variable density; hard │
│                      │ connected            │ fraud detection        │ to tune $\epsilon$     │
├──────────────────────┼──────────────────────┼────────────────────────┼────────────────────────┤
│ Gaussian Mixture     │ Ellipsoidal, soft    │ Overlapping clusters;  │ Expectation-Max        │
│ Models (GMM)         │ probabilistic        │ uncertainty modeling;  │ sensitive to initial-  │
│                      │ memberships          │ generative modeling    │ ization; covariance fit│
└──────────────────────┴──────────────────────┴────────────────────────┴────────────────────────┘
```

---

## 9. How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Pankaj-Shinde-07/MDM_AI-ML_AS06.git
   cd MDM_AI-ML_AS06
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute the clustering pipeline:**
   ```bash
   python clustering_algorithms.py
   ```
   All diagnostic plots will be exported to `screenshots/`, and numerical evaluation reports written to `sample_io/`.
