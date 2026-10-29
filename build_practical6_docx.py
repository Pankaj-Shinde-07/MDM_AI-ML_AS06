"""
Script to build the publication-grade Word document (.docx) and PDF (.pdf)
for Practical Assignment 6: Clustering Algorithms.
Student: Pankaj Shinde (PRN: 202401100005)
Faculty: Dr. Khushal Khairnar
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx2pdf import convert

BASE_DIR = r"d:\TY subjects\MDM-AIML-Lab\Practical 6"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "clustering_algorithms", "screenshots")
OUTPUT_DOCX = os.path.join(BASE_DIR, "Practical Assignment 6 - Clustering Algorithms.docx")
OUTPUT_PDF = os.path.join(BASE_DIR, "Practical Assignment 6 - Clustering Algorithms.pdf")
ROOT_DOCX = r"d:\TY subjects\MDM-AIML-Lab\MDM AIML Assignment 6.docx"
ROOT_PDF = r"d:\TY subjects\MDM-AIML-Lab\MDM AIML Assignment 6.pdf"


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)


def style_table(table, col_widths, header_bg="2B5C8F", zebra=False):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    for row_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        if row_idx == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for c_idx, cell in enumerate(row.cells):
            cell.width = Inches(col_widths[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

            if row_idx == 0 and header_bg:
                set_cell_shading(cell, header_bg)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.bold = True
                        r.font.name = "Times New Roman"
                        r.font.color.rgb = RGBColor(255, 255, 255)
            elif zebra and row_idx % 2 == 1:
                set_cell_shading(cell, "F2F4F4")


def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(21, 67, 96)
    return p


def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(40, 55, 71)
    return p


def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = Pt(14)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(27, 38, 59)

    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(11)
    r_body.font.color.rgb = RGBColor(33, 33, 33)
    return p


def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = Pt(13.5)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(27, 38, 59)

    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = RGBColor(33, 33, 33)
    return p


def add_figure(doc, img_name, caption_text, width_inches=6.2):
    img_path = os.path.join(SCREENSHOTS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.paragraph_format.keep_with_next = True
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Times New Roman"
        run_cap.font.size = Pt(9.5)
        run_cap.font.bold = True
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(86, 101, 115)


def generate_practical_6_docx():
    print("[1/4] Initializing Practical 6 Document...")
    doc = docx.Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    r1 = p_title.add_run("TY B.Tech. – ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(21, 67, 96)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    r2 = p_sub.add_run("PRACTICAL ASSIGNMENT 6: CLUSTERING ALGORITHMS & QUALITY EVALUATION")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(40, 55, 71)

    # 1. Student Details
    add_heading_1(doc, "1. Student Details")
    t0 = doc.add_table(rows=7, cols=2)
    t0.style = 'Table Grid'
    t0_data = [
        ("Student Name", "Pankaj Shinde"),
        ("PRN", "202401100005"),
        ("Branch", "Software Engineering"),
        ("Division", "A"),
        ("Batch", "A1"),
        ("Roll No.", "07"),
        ("Date of Submission", "28-10-2026")
    ]
    for idx, (k, v) in enumerate(t0_data):
        row = t0.rows[idx]
        row.cells[0].paragraphs[0].add_run(k).font.bold = True
        row.cells[1].paragraphs[0].add_run(v)
    style_table(t0, [2.5, 4.3], header_bg=None)

    # 2. Practical Details
    add_heading_1(doc, "2. Practical Details")
    t1 = doc.add_table(rows=4, cols=2)
    t1.style = 'Table Grid'
    t1_data = [
        ("Practical No.", "6"),
        ("Practical Title", "Implementation and Quality Evaluation of Clustering Algorithms (K-Means, Hierarchical Agglomerative, DBSCAN) on Real-World Data"),
        ("Date Performed", "24-10-2026"),
        ("Faculty Name", "Dr. Khushal Khairnar")
    ]
    for idx, (k, v) in enumerate(t1_data):
        row = t1.rows[idx]
        row.cells[0].paragraphs[0].add_run(k).font.bold = True
        row.cells[1].paragraphs[0].add_run(v)
    style_table(t1, [2.5, 4.3], header_bg=None)

    # 3. Problem Statement
    add_heading_1(doc, "3. Problem Statement")
    add_body_p(doc,
               '"Implement clustering algorithms on a real-world dataset to identify meaningful groups within the data. Evaluate the quality of clustering results using appropriate metrics such as silhouette score, Davies Bouldin index, or visual inspection."',
               bold_prefix="Problem Statement: ")
    add_body_p(doc,
               "Unsupervised Machine Learning focuses on discovering latent patterns, intrinsic structural regularities, and natural groupings in unlabelled data. Unlike supervised classification where ground-truth targets guide parameter optimization, clustering algorithms partition data based on geometric proximity, connectivity, or density distributions. Different clustering paradigms operate under fundamentally distinct mathematical assumptions: K-Means partitions feature space into Voronoi cells minimizing within-cluster variance, Hierarchical Agglomerative clustering constructs a multi-scale connectivity tree, while DBSCAN (Density-Based Spatial Clustering of Applications with Noise) identifies dense connected manifolds capable of discovering arbitrary non-linear shapes while filtering out noise.")
    add_body_p(doc,
               "This practical focuses on implementing an end-to-end unsupervised cluster analysis pipeline on the real-world Mall Customer Segmentation Dataset. The objectives are to implement and compare K-Means (with K-Means++ initialization), Hierarchical Agglomerative Clustering (Ward's criterion), DBSCAN, and Gaussian Mixture Models (GMM). Clustering quality is rigorously evaluated using the Elbow Method, Silhouette Score analysis, Davies-Bouldin Index, Calinski-Harabasz Index, and visual inspections in two-dimensional behavioral feature space (Annual Income vs. Spending Score), culminating in actionable commercial customer persona profiles.")

    # 4. Objectives
    add_heading_1(doc, "4. Objectives")
    objectives = [
        ("1. Clustering Paradigms Implementation: ", "To implement and contrast three distinct clustering paradigms: Centroid-based (K-Means++), Connectivity-based (Hierarchical Agglomerative with Ward linkage), and Density-based (DBSCAN) using Scikit-Learn."),
        ("2. Real-World Unsupervised Data Pipeline: ", "To execute an end-to-end unsupervised pipeline on the Mall Customer Segmentation dataset, including feature extraction, StandardScaler normalization, and cluster centroid tracking."),
        ("3. Optimal Hyperparameter Determination: ", "To determine the optimal number of clusters K through the Elbow Method (Within-Cluster Sum of Squares) and Silhouette score sweeps across k in [2, 10], and select optimal epsilon for DBSCAN via K-nearest neighbors distance elbow curves."),
        ("4. Quantitative Quality Evaluation: ", "To compute, benchmark, and interpret foundational internal clustering validation indices: Silhouette Score, Davies-Bouldin Index, and Calinski-Harabasz Index."),
        ("5. Diagnostic Visualization: ", "To generate publication-grade visual diagnostics: Dual-axis Elbow/Silhouette sweeps, 2D centroid scatter maps, Hierarchical dendrograms with cut-off thresholds, sample-level silhouette coefficient plots, and demographic boxplots."),
        ("6. Business Persona Profiling: ", "To translate unsupervised geometric clusters into actionable commercial consumer personas (Budget, Impulsive, Moderate, VIP Target, and Savers) with strategic marketing implications.")
    ]
    for pre, obj in objectives:
        add_bullet_p(doc, obj, bold_prefix=pre)

    # 5. Expected Learning Outcomes
    add_heading_1(doc, "5. Expected Learning Outcomes")
    add_body_p(doc, "After completing this practical assignment, the student will be able to:")
    outcomes = [
        ("1. Distinguish Clustering Paradigms: ", "Explain the core mathematical mechanics, inductive biases, and geometric assumptions of partitioning, hierarchical, and density-based clustering algorithms."),
        ("2. Master K-Means++ Initialization: ", "Explain how K-Means++ probabilistic distance-squared seeding eliminates poor local minima traps compared to standard random centroid initialization."),
        ("3. Interpret Hierarchical Trees (Dendrograms): ", "Read and analyze hierarchical dendrograms to understand multi-scale cluster merges and select mathematically sound cophenetic distance thresholds."),
        ("4. Apply Density-Based Spatial Clustering: ", "Understand how DBSCAN discovers clusters of arbitrary non-convex geometries and how core distance thresholds isolate isolated noise samples."),
        ("5. Critically Evaluate Unsupervised Metrics: ", "Differentiate between Silhouette Score (compactness and separation), Davies-Bouldin Index (cluster dispersion ratio), and Calinski-Harabasz Index (variance ratio criterion) to evaluate cluster validity without ground truth.")
    ]
    for pre, out in outcomes:
        add_bullet_p(doc, out, bold_prefix=pre)

    # 6. Theory & Architectural Concepts
    add_heading_1(doc, "6. Theory & Architectural Concepts")

    add_heading_2(doc, "6.1 Overview of Unsupervised Clustering")
    add_body_p(doc,
               "Clustering is the unsupervised task of partitioning an unlabeled dataset D = {x_1, x_2, ..., x_N} in R^d into K disjoint (or fuzzy) subsets C = {C_1, C_2, ..., C_K} such that instances within the same group share high similarity, while instances in different groups exhibit maximum dissimilarity. Unlike supervised learning, no objective ground-truth target y_i is available during training. The three major algorithmic paradigms investigated are:")
    add_bullet_p(doc, "Partitioning Methods (K-Means): Construct K discrete partitions minimizing an objective distance function.", bold_prefix="• ")
    add_bullet_p(doc, "Hierarchical Methods (Agglomerative): Build a nested hierarchical tree of clusters via iterative bottom-up merging.", bold_prefix="• ")
    add_bullet_p(doc, "Density-Based Methods (DBSCAN): Discover arbitrarily shaped clusters as dense continuous regions separated by low-density noise regions.", bold_prefix="• ")

    add_heading_2(doc, "6.2 K-Means Clustering & K-Means++ Initialization")
    add_body_p(doc,
               "K-Means partitions N observations into K clusters by minimizing the Within-Cluster Sum of Squares (WCSS or Inertia):")
    add_body_p(doc,
               "J = sum_{k=1}^K sum_{x_i in C_k} ||x_i - mu_k||^2",
               bold_prefix="Objective Function (Inertia): ")
    add_body_p(doc,
               "Where mu_k is the geometric mean (centroid) of cluster C_k. Standard Lloyd's algorithm alternates between two steps: (1) Assignment step: assign each point x_i to the nearest centroid; (2) Update step: recalculate centroids as the arithmetic mean of assigned points. Because random initialization frequently converges to suboptimal local minima, K-Means++ initializes centroids sequentially: the first centroid is chosen uniformly at random, and subsequent centroids are chosen with probability proportional to the squared Euclidean distance D(x)^2 to the nearest existing center, ensuring well-dispersed initial centroids.")

    add_heading_2(doc, "6.3 Hierarchical Agglomerative Clustering (Ward's Method)")
    add_body_p(doc,
               "Hierarchical Agglomerative Clustering (HAC) is a bottom-up approach where every data point begins as its own singleton cluster. At each iteration, the two clusters that minimize a linkage distance metric are merged, continuing until a single root cluster remains. Under Ward's Minimum Variance Linkage, the cost of merging cluster A and B is the increase in the total sum of squares:")
    add_body_p(doc,
               "Delta ESS_{A,B} = [ (n_A * n_B) / (n_A + n_B) ] * ||mu_A - mu_B||^2",
               bold_prefix="Ward's Criterion: ")
    add_body_p(doc,
               "Ward's criterion creates compact, balanced clusters with minimal within-cluster variance. The entire sequence of merges is recorded as a Dendrogram, allowing the practitioner to inspect clustering hierarchies across all spatial scales.")

    add_heading_2(doc, "6.4 DBSCAN (Density-Based Spatial Clustering)")
    add_body_p(doc,
               "DBSCAN (Ester et al., 1996) defines clusters as continuous high-density areas separated by areas of low density. It requires two primary hyperparameters: epsilon (the maximum radius of a neighborhood) and MinPts (the minimum number of points required to form a dense region). Points are categorized into three distinct roles:")
    add_bullet_p(doc, "Core Point: A point p is a core point if |N_eps(p)| >= MinPts, where N_eps(p) = {q in D | dist(p, q) <= eps}.", bold_prefix="• ")
    add_bullet_p(doc, "Border Point: A point that is within distance eps of a core point but contains fewer than MinPts neighbors.", bold_prefix="• ")
    add_bullet_p(doc, "Noise Point: A point that is neither a core point nor reachable from any core point (labeled as -1).", bold_prefix="• ")
    add_body_p(doc,
               "Key advantages of DBSCAN include: (1) no requirement to specify the number of clusters K a priori; (2) ability to discover clusters of arbitrary, non-spherical shapes; and (3) native resistance to noise and outliers.")

    add_heading_2(doc, "6.5 Internal Quality Validation Metrics")
    add_body_p(doc,
               "To validate cluster quality without ground-truth labels, the following mathematical metrics are computed:")
    add_bullet_p(doc, "Silhouette Score (s in [-1, +1]): For point i, s(i) = (b(i) - a(i)) / max(a(i), b(i)), where a(i) is mean intra-cluster distance and b(i) is mean distance to nearest neighboring cluster. Values close to +1 indicate dense, well-isolated clusters.", bold_prefix="• Silhouette Score: ")
    add_bullet_p(doc, "Davies-Bouldin Index (DB >= 0): DB = (1/K) sum_{i=1}^K max_{j != i} ( (s_i + s_j) / d(c_i, c_j) ), where s_i is cluster dispersion and d is centroid distance. Lower scores indicate superior separation.", bold_prefix="• Davies-Bouldin Index: ")
    add_bullet_p(doc, "Calinski-Harabasz Index (CH): Ratio of between-cluster variance to within-cluster variance: CH = [ Tr(B_K) / (K - 1) ] / [ Tr(W_K) / (N - K) ]. Higher values indicate compact, well-separated clusters.", bold_prefix="• Calinski-Harabasz Index: ")

    # 7. Algorithm & Pipeline Workflow
    add_heading_1(doc, "7. Algorithm & Pipeline Workflow")
    add_body_p(doc, "START CLUSTERING PIPELINE\n"
                    "Step 1: Load 200 customer records from Mall Customer Segmentation Dataset.\n"
                    "Step 2: Extract behavioral feature matrix X = [Annual Income (k$), Spending Score (1-100)].\n"
                    "Step 3: Standardize features with StandardScaler (z = (x - mu) / sigma) to equalize scales.\n"
                    "Step 4: Execute K-Means parameter sweep across k in [2, 10]:\n"
                    "        - Compute Inertia (WCSS) to construct the Elbow Curve.\n"
                    "        - Compute Silhouette Score curve to verify global separation peak.\n"
                    "Step 5: Fit optimal K-Means model (k=5, init='k-means++', n_init=20) and compute inverse-scaled centroids.\n"
                    "Step 6: Construct Hierarchical Agglomerative tree using Ward Linkage and render full Dendrogram.\n"
                    "Step 7: Perform K-NN distance plot (k=5) to detect knee for DBSCAN epsilon parameterization (eps=0.35).\n"
                    "Step 8: Fit DBSCAN and categorize Core, Border, and Noise (-1) outlier samples.\n"
                    "Step 9: Fit Gaussian Mixture Model (k=5, EM) as soft probabilistic benchmark.\n"
                    "Step 10: Compute Silhouette Score, Davies-Bouldin Index, and Calinski-Harabasz Index across all algorithms.\n"
                    "Step 11: Generate 8 publication-grade diagnostic plots.\n"
                    "Step 12: Aggregate customer profiles and construct actionable business marketing personas.\n"
                    "STOP CLUSTERING PIPELINE")

    # 8. Experimental Results
    add_heading_1(doc, "8. Experimental Results & Quantitative Evaluation")
    add_body_p(doc,
               "The quantitative evaluation metrics across the four clustering algorithms on the standardized customer segmentation dataset are summarized below:")

    t_res = doc.add_table(rows=5, cols=7)
    t_res.style = 'Table Grid'
    headers = ["Clustering Algorithm", "Paradigm", "Clusters (k)", "Noise Points", "Silhouette", "Davies-Bouldin", "Calinski-Harabasz"]
    for c_idx, h in enumerate(headers):
        t_res.rows[0].cells[c_idx].paragraphs[0].add_run(h)

    res_data = [
        ("DBSCAN (eps=0.35, min=5)", "Density-Based", "5", "27", "0.6347", "0.4359", "354.50"),
        ("K-Means (k=5, k-means++)", "Centroid-Based", "5", "0", "0.5844", "0.5126", "315.69"),
        ("Gaussian Mixture Model (k=5)", "Probabilistic (EM)", "5", "0", "0.5834", "0.5104", "307.78"),
        ("Hierarchical Agglomerative (Ward)", "Connectivity-Based", "5", "0", "0.5748", "0.5214", "301.95")
    ]

    for r_idx, row_vals in enumerate(res_data):
        row = t_res.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            p = row.cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx >= 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            if r_idx in [0, 1]:
                r.font.bold = True
    style_table(t_res, [1.8, 1.1, 0.7, 0.7, 0.75, 0.85, 0.9], header_bg="2B5C8F", zebra=True)

    add_body_p(doc, "Analysis of Empirical Clustering Indices:")
    add_bullet_p(doc, "Superiority of K=5 Partition: In the K-Means hyperparameter sweep, WCSS drops precipitously until k=5 (53.51), after which the rate of variance reduction plateaus, confirming the classic elbow knee. Concurrently, the Silhouette Score peaks at 0.5844 for k=5, demonstrating optimal cluster cohesion and separation.", bold_prefix="• ")
    add_bullet_p(doc, "DBSCAN Noise Filtering: DBSCAN achieved the highest Silhouette Score (0.6347) and lowest Davies-Bouldin Index (0.4359). This occurs because DBSCAN isolates 27 ambiguous boundary points as noise (-1), evaluating only dense core cluster cores.", bold_prefix="• ")
    add_bullet_p(doc, "Structural Agreement between K-Means and Ward's HAC: K-Means (Silhouette 0.5844) and Ward's Agglomerative Clustering (Silhouette 0.5748) demonstrate virtually identical spatial cluster boundaries, validating that the underlying customer data exhibits convex, naturally separated clusters.", bold_prefix="• ")

    # 9. Actionable Customer Persona Segmentation Table
    add_heading_1(doc, "9. Actionable Customer Persona Segmentation")
    add_body_p(doc,
               "By projecting the discovered clusters back onto original dollar and spending score scales, five distinct commercial customer personas were synthesized:")

    t_pers = doc.add_table(rows=6, cols=6)
    t_pers.style = 'Table Grid'
    p_heads = ["Cluster", "Persona Title", "Customer Count", "Mean Income", "Mean Spending", "Actionable Business Strategy"]
    for idx, h in enumerate(p_heads):
        t_pers.rows[0].cells[idx].paragraphs[0].add_run(h)

    p_data = [
        ("Cluster 1", "Sensible / Budget", "23 (11.5%)", "$26.3k", "20.9 / 100", "Discount vouchers, budget loyalty programs, essential goods promotion."),
        ("Cluster 2", "Careless / Impulsive", "22 (11.0%)", "$25.7k", "79.4 / 100", "Trendy fashion sales, gamified rewards, instalment financing options."),
        ("Cluster 3", "Standard / Moderate", "81 (40.5%)", "$55.3k", "49.5 / 100", "Middle-class retail backbone; family seasonal deals, staple retail discounts."),
        ("Cluster 4", "Affluent / Target (VIP)", "39 (19.5%)", "$86.5k", "82.1 / 100", "High-value primary target: Luxury previews, VIP concierge, fine dining events."),
        ("Cluster 5", "Careful / Savers", "35 (17.5%)", "$88.2k", "17.1 / 100", "Quality-focused marketing, durable luxury goods, investment/wealth products.")
    ]
    for r_idx, row_vals in enumerate(p_data):
        row = t_pers.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            p = row.cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            row.cells[c_idx].paragraphs[0].add_run(val)
    style_table(t_pers, [0.8, 1.4, 0.9, 0.9, 0.9, 1.9], header_bg="2B5C8F", zebra=True)

    # 10. Diagnostic Visualizations & Analysis
    add_heading_1(doc, "10. Diagnostic Visualizations & Analysis")

    add_figure(doc, "01_kmeans_elbow_and_silhouette_sweep.png",
               "Figure 6.1: Dual-Axis K-Means Hyperparameter Optimization: Inertia (WCSS) Elbow Curve and Silhouette Score Sweep across k in [2, 10].")
    add_body_p(doc,
               "Figure 6.1 displays the parameter selection landscape. The blue curve illustrates the Elbow Method: inertia drops dramatically from 258.70 (k=2) to 53.51 (k=5), after which the curve levels off. Concurrently, the dashed green Silhouette curve peaks at k=5 (0.5844), providing mathematical proof that five clusters form the optimal partitioning.")

    add_figure(doc, "02_kmeans_clusters_2d_centroids.png",
               "Figure 6.2: 2D Spatial Customer Clusters with Color-Coded Personas and Annotated Centroids.")
    add_body_p(doc,
               "Figure 6.2 plots customers along Annual Income vs. Spending Score. Yellow stars mark the geometric centroids. The five distinct quadrants and center cluster correspond precisely to commercial customer archetypes.")

    add_figure(doc, "03_hierarchical_dendrogram.png",
               "Figure 6.3: Hierarchical Agglomerative Clustering Dendrogram using Ward Linkage with Cut-Off Threshold.")
    add_body_p(doc,
               "Figure 6.3 presents the hierarchical tree. The vertical axis represents cophenetic Euclidean distance between merged clusters. The horizontal dashed red line at distance threshold 5.0 cuts across five vertical branches, corroborating the K-Means finding.")

    add_figure(doc, "04_hierarchical_vs_kmeans_comparison.png",
               "Figure 6.4: Structural Comparison: K-Means (k=5) vs. Hierarchical Agglomerative Clustering (k=5).")
    add_body_p(doc,
               "Figure 6.4 displays side-by-side scatter plots. Both algorithms yield near-identical cluster allocations, proving that the five customer segments are robust to algorithm choice.")

    add_figure(doc, "05_dbscan_k_distance_and_clusters.png",
               "Figure 6.5: DBSCAN 5-Nearest Neighbor Distance Elbow Curve (Left) and Density-Based Cluster Assignments with Noise Points (Right).")
    add_body_p(doc,
               "Figure 6.5 illustrates DBSCAN parameterization. The left panel shows the 5-NN distance curve with an elbow knee at epsilon=0.35. The right panel shows the resulting clusters, identifying five dense clusters and isolating 27 peripheral points as noise (marked with black crosses).")

    add_figure(doc, "06_silhouette_analysis_per_cluster.png",
               "Figure 6.6: Comprehensive Silhouette Coefficient Plot for Individual Customers across K-Means Clusters.")
    add_body_p(doc,
               "Figure 6.6 presents silhouette coefficients for individual instances. The dashed red vertical line denotes the average silhouette score (0.5844). All five clusters possess consistent silhouette widths with virtually no negative values, confirming optimal cluster cohesion.")

    add_figure(doc, "07_clustering_metrics_comparison_bar.png",
               "Figure 6.7: Quantitative Quality Metrics Comparison (Silhouette, Davies-Bouldin, Calinski-Harabasz) across Algorithms.")
    add_body_p(doc,
               "Figure 6.7 provides a tri-panel comparative bar chart. Across all three metrics, K-Means, Ward HAC, and GMM demonstrate tightly matched performance, while DBSCAN achieves the highest silhouette and lowest Davies-Bouldin index due to outlier isolation.")

    add_figure(doc, "08_cluster_business_personas.png",
               "Figure 6.8: Boxplot Demographic Distributions of Annual Income and Spending Score across Discovered Clusters.")
    add_body_p(doc,
               "Figure 6.8 shows distribution boxplots for each cluster. Non-overlapping interquartile ranges (IQR) across income and spending confirm clean separation between consumer classes.")

    # 11. Comparative Paradigm Analysis
    add_heading_1(doc, "11. Comparative Analysis & Strategic Algorithm Selection")
    add_body_p(doc,
               "Different clustering algorithms are designed for distinct geometric topologies and operational constraints:")

    t_comp = doc.add_table(rows=5, cols=4)
    t_comp.style = 'Table Grid'
    c_heads = ["Clustering Algorithm", "Cluster Topology", "Ideal Use Case", "Operational Limitations"]
    for idx, h in enumerate(c_heads):
        t_comp.rows[0].cells[idx].paragraphs[0].add_run(h)

    c_data = [
        ("K-Means++",
         "Convex, spherical, isotropic clusters with comparable variance.",
         "High-throughput customer segmentation; large tabular datasets where compute efficiency (O(N*k*d)) is mandatory.",
         "Requires specifying K upfront; sensitive to non-spherical geometries and extreme outliers."),
        ("Hierarchical Agglomerative",
         "Hierarchical taxonomies; nested multi-scale clusters.",
         "Taxonomic biological classification; small-to-medium datasets (< 5,000 samples) where visual dendrogram is required.",
         "Computationally heavy (O(N^2) memory, O(N^3) time); merge decisions are greedy and irreversible."),
        ("DBSCAN",
         "Arbitrary non-convex shapes; density-connected manifolds.",
         "Spatial geospatial data; GPS trajectory analysis; anomaly and fraud detection where noise isolation is critical.",
         "Degrades on datasets with variable densities; sensitive to epsilon and MinPts hyperparameter tuning."),
        ("Gaussian Mixture Models",
         "Ellipsoidal clusters with soft probabilistic boundaries.",
         "Overlapping clusters; generative data modeling; applications requiring posterior probability belongingness.",
         "Expectation-Maximization can get trapped in local singularities; requires covariance matrix estimation.")
    ]
    for r_idx, row_vals in enumerate(c_data):
        row = t_comp.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            p = row.cells[c_idx].paragraphs[0]
            p.add_run(val)
    style_table(t_comp, [1.5, 1.6, 2.0, 1.7], header_bg="2B5C8F", zebra=True)

    # 12. Areas for Further Research
    add_heading_1(doc, "12. Areas for Further Research & Algorithmic Improvements")
    res_pts = [
        ("1. HDBSCAN (Hierarchical Density-Based Clustering): ", "Extending DBSCAN with HDBSCAN, which converts DBSCAN into a hierarchical clustering algorithm to find clusters of varying densities automatically without specifying epsilon."),
        ("2. Deep Embedding Clustering (DEC): ", "Applying Deep Autoencoders to learn low-dimensional latent representations simultaneously with clustering objective optimization."),
        ("3. Spectral Clustering on Complex Manifolds: ", "Using Graph Laplacian spectral decomposition to cluster complex non-linear manifolds that fail under Euclidean distance."),
        ("4. High-Dimensional Dimensionality Reduction: ", "Benchmarking UMAP (Uniform Manifold Approximation and Projection) and t-SNE for pre-clustering dimensionality reduction on complex customer behavioral vectors.")
    ]
    for pre, pt in res_pts:
        add_bullet_p(doc, pt, bold_prefix=pre)

    # 13. Conclusion
    add_heading_1(doc, "13. Conclusion")
    add_body_p(doc,
               "In this practical assignment, three foundational clustering paradigms—Centroid-based (K-Means++), Connectivity-based (Hierarchical Agglomerative with Ward linkage), and Density-based (DBSCAN)—were successfully implemented, evaluated, and contrasted on the real-world Mall Customer Segmentation Dataset alongside Gaussian Mixture Models. Both the Elbow Method and Silhouette Analysis conclusively verified that K=5 represents the natural clustering structure, achieving a high Silhouette Score of 0.5844. DBSCAN demonstrated exceptional ability to isolate 27 peripheral noise outliers, boosting core silhouette quality to 0.6347. The resulting customer clusters provided actionable commercial segmentation profiles (Sensible, Impulsive, Standard, VIP Target, and Savers), confirming the practical utility of unsupervised learning in data-driven commercial strategy.")

    # 14. References
    add_heading_1(doc, "14. References")
    refs = [
        "MacQueen, J. (1967). 'Some methods for classification and analysis of multivariate observations.' Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, 1(14), 281-297.",
        "Arthur, D., & Vassilvitskii, S. (2007). 'k-means++: The advantages of careful seeding.' Proceedings of the Eighteenth Annual ACM-SIAM Symposium on Discrete Algorithms, 1027-1035.",
        "Ward, J. H. (1963). 'Hierarchical grouping to optimize an objective function.' Journal of the American Statistical Association, 58(301), 236-244.",
        "Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). 'A density-based algorithm for discovering clusters in large spatial databases with noise.' KDD, 96(34), 226-231.",
        "Rousseeuw, P. J. (1987). 'Silhouettes: a graphical aid to the interpretation and validation of cluster analysis.' Journal of Computational and Applied Mathematics, 20, 53-65.",
        "Davies, D. L., & Bouldin, D. W. (1979). 'A cluster separation measure.' IEEE Transactions on Pattern Analysis and Machine Intelligence, (2), 224-227."
    ]
    for r in refs:
        add_bullet_p(doc, r, bold_prefix="• ")

    # Save Word document
    print(f"[2/4] Saving DOCX to {OUTPUT_DOCX}...")
    doc.save(OUTPUT_DOCX)
    print(f"[3/4] Copying DOCX to root {ROOT_DOCX}...")
    doc.save(ROOT_DOCX)

    # Convert to PDF
    print(f"[4/4] Converting DOCX to PDF using docx2pdf...")
    try:
        convert(OUTPUT_DOCX, OUTPUT_PDF)
        print(f"Successfully generated: {OUTPUT_PDF}")
        convert(ROOT_DOCX, ROOT_PDF)
        print(f"Successfully generated: {ROOT_PDF}")
    except Exception as e:
        print(f"Warning: PDF conversion encountered: {e}")

    print("\n[SUCCESS] Practical 6 documentation generation finished!")


if __name__ == "__main__":
    generate_practical_6_docx()
