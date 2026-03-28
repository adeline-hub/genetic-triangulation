# Project: Genetic Triangulation Engine (GTE)

*data science to genealogy*



**Objective**: To systematically map autosomal DNA segments to verify ancestral lineages, perform ethnic clustering, and identify unknown biological connections (e.g., potential half-siblings/paternal-maternal lines) through triangulation.




## The Forensic Workflow



Data genealogy is the practice of converting "noise" (thousands of distant matches) into "signal" (validated common ancestors). This engine follows a four-stage forensic process:



1. **Ingestion & Normalization**: Standardizing disparate GedMatch exports into a uniform coordinate system.

2. **Heuristic Classification**: Leveraging metadata (email domains, surname etymology, test providers) to establish a "Likely Origin" probability for each match.

3. **Triangulation Engine**: Executing interval intersection math to identify segments shared by the Target ID and at least two other matches, confirming a common ancestor.

4. **Cluster Synthesis**: Aggregating segments by "Lineage Cluster" to visualize geographical patterns across chromosomes.



## Investigative Pipeline



* `data/`: Contains raw CSV exports from GedMatch (e.g., one\_to\_many\_results.csv, shared_segments.csv).

* `src/cleaner.py`: Performs data hygiene (removing duplicate test IDs, correcting data types).

* `src/classifier.py`: Applies demographic weighting based on surname provenance and email suffixes.

* `src/analyzer.py`: Runs the intersection logic (The "Smoking Gun" finder).

* `src/visualize.py`: Renders the Chromosome Browser for visual cluster verification.


## Run the analysis

**CLI Command**
cd local folder
python app.py


<div align="center">
  <!-- REPLACE THE LINK BELOW WITH YOUR ACTUAL PHOTO URL -->
  <img src="https://github.com/adeline-hub/genetic-triangulation/blob/main/Tringulation-toolkitv1.png?raw=true" alt="genetic-triangulation" style="border-radius: 50%; width: 200px; height: 200px;">
</div>
## Disclaimer

Genetic data is personal health information. This toolkit operates locally to ensure your raw genomic data is never transmitted to third-party cloud servers. Use responsibly when investigating sensitive family history.



*   [**`genetic-triangulation`**](https://github.com/adeline-hub/genetic-triangulation)

