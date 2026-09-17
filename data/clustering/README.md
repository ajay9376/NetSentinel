# Clustering Track Dataset Documentation

## Dataset Name
**CTU-13**

## Track
**Track 3: Clustering**

## Objective
To perform unsupervised exploratory profiling and behavioral clustering on network traffic flows, identifying anomalous communication structures, botnet activity clusters, and background patterns without relying on supervised ground-truth labels during model training.

## Dataset Source & Attribution
- **Provider**: Stratosphere IPS Project / Czech Technical University (CTU)
- **Official Portal**: [https://www.stratosphereips.org/datasets-ctu13](https://www.stratosphereips.org/datasets-ctu13)

## Expected Local File(s)
- CTU-13 scenario flow file(s) (e.g., `capture20110810.binetflow` or converted NetFlow CSV files from selected scenarios).

## Setup Instructions
1. Download the CTU-13 scenario files from the official Stratosphere IPS archive.
2. Place the converted CSV or binetflow file(s) directly into this directory (`data/clustering/`).
3. Verify that the file format aligns with the preprocessing pipeline in `notebooks/clustering.ipynb`.

> [!NOTE]
> No dataset files are automatically downloaded or pre-populated in this directory. Users are responsible for acquiring and placing the verified dataset files here.
