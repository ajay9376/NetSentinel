# Regression Track Dataset Documentation

## Dataset Name
**UNSW-NB15**

## Track
**Track 1: Regression**

## Objective
To predict continuous Quality of Service (QoS) and network degradation indicators—specifically Source Packet Loss (`sloss`) or related latency/throughput flow parameters—based on raw and engineered network packet flow attributes.

## Dataset Source & Attribution
- **Provider**: Cyber Range Lab of the Australian Centre for Cyber Security (ACCS) / UNSW Canberra
- **Official Portal**: [https://research.unsw.edu.au/projects/unsw-nb15-dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset)

## Expected Local File(s)
- `UNSW_NB15_training-set.csv` (or selected UNSW-NB15 flow CSV files)

## Setup Instructions
1. Obtain the official UNSW-NB15 dataset from the ACCS provider portal.
2. Place the CSV file(s) directly inside this folder (`data/regression/`).
3. Ensure file naming matches the ingestion paths referenced in `notebooks/regression.ipynb`.

> [!NOTE]
> No dataset files are automatically downloaded or pre-populated in this directory. Users are responsible for acquiring and placing the verified dataset files here.
