# Clustering Track Dataset Documentation

## Primary Benchmark Dataset
**NSL-KDD (`nslkdd.csv`)**

## Track
**Track 3: Clustering (Unsupervised Network Traffic Profiling)**

## Objective
To perform unsupervised exploratory profiling and behavioral clustering on network traffic flows, identifying anomalous communication structures, volumetric attack clusters (DoS, probe), and normal background patterns without relying on supervised ground-truth labels during model training.

## Dataset Specifications
- **File**: `data/clustering/nslkdd.csv`
- **Total Flow Records**: 140,772 rows
- **Feature Space**: 41 network traffic features (protocols, duration, error rates, service categories)
- **Primary Evaluated Algorithms**: K-Means ($K=5$), Agglomerative Hierarchical Clustering, PCA, and t-SNE

## Secondary Reference Dataset
- **Name**: CTU-13 (Botnet Traffic Scenarios)
- **Source**: Stratosphere IPS Project / Czech Technical University (CTU)
- **Portal**: [https://www.stratosphereips.org/datasets-ctu13](https://www.stratosphereips.org/datasets-ctu13)

