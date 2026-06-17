# bibMining

This is the repository of the scripts employed in 'Mining and Floods: A Systematic Review of Empirical Studies on Community Resilience Strategies and Interventions', available at the publisher's site [here](https://doi.org/10.1016/j.exis.2026.101984).


**NOTE**: The related OSF repository is available [here](https://osf.io/85ucn).


## Content

* `src/keyword_clustering.ipynb`: generates a keywords clustering of the studies. The output file is in EPS format.

* `src/histo_num_papers.ipynb`: generates a histogram of the number of papers published per year in the corpus. The output file is in EPS format.

* `src/map_articles.ipynb`: generates a map of the studies. The output file is in EPS format.

* `src/citation_network.ipynb`: generates a co-citation graph of the corpus. The output are in PDF and PGF formats.

* `src/inter_rater.ipynb`: computes the inter-rater reliability statistics given the excel file 'Ration-Dimension.xlsx', using Cohen's kappa.

* `src/screening.ipynb`: cleans data from raw Scopus and WoS queries results.