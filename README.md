## Overview

This script generates weekly and yearly line graphs from AI-powered foot traffic data collected in Takayama City.  
Our hope is that this project serves as both a gateway for discovering the fun of IT and a small contribution to revitalizing the local community.

- **Total Data**: 166 weeks (48 weeks × 5 years + extra)
- **Estimated Processing Time**: \~233 seconds

## Environment

- **OS**: Windows 11
- **Anaconda Version**: conda 23.7.4

## Libraries

- `pandas`
- `matplotlib`

## To Do

1. Download the target CSV file from the site listed in \[1].
2. Place the file in the `csv_path` specified on line 9 of the script.
3. Run `1_weekly_insights.py`.
4. The output will be generated in two folders:

   - `weekly_graphs_by_year`: line graphs by year
   - `weekly_csv_by_year`: processed CSV files by year

\[1] **AI-based Foot Traffic Measurement (Japanese)**
[https://www.city.takayama.lg.jp/shisei/1000062/1004915/1012977/index.html](https://www.city.takayama.lg.jp/shisei/1000062/1004915/1012977/index.html)

## Output

The generated results are already available at the following link:

**Output Folder (Google Drive)**  
[https://drive.google.com/drive/folders/12J0Ut4_rL9CCdnXQBoKNtKa95G_nqAh3?usp=sharing](https://drive.google.com/drive/folders/12J0Ut4_rL9CCdnXQBoKNtKa95G_nqAh3?usp=sharing)
