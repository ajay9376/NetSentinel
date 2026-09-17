# Classification Track Dataset Documentation

## Dataset Name
**CIC-IDS2017**

## Track
**Track 2: Classification**

## Objective
To categorize network communication flows into multi-class intrusion categories (such as DoS/DDoS, PortScan, Brute Force, Web Attacks, Infiltration) as well as benign network traffic, evaluating precision, recall, and detection accuracy across varied threat profiles.

## Dataset Source & Attribution
- **Provider**: Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB)
- **Official Portal**: [https://www.unb.ca/cic/datasets/ids-2017.html](https://www.unb.ca/cic/datasets/ids-2017.html)

## Expected Local File(s)
- Extracted CSV files from the `GeneratedLabelledFlows` archive (e.g., `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`, `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`, or consolidated traffic CSVs).

## Setup Instructions
1. Download the CIC-IDS2017 dataset archive from the official UNB website.
2. Extract the designated CSV files and place them into this directory (`data/classification/`).
3. Ensure the CSV filenames align with the data loader specifications in `notebooks/classification.ipynb`.

> [!NOTE]
> No dataset files are automatically downloaded or pre-populated in this directory. Users are responsible for acquiring and placing the verified dataset files here.
