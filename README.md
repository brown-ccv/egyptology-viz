# egyptology-viz
### Background
This project aims to implement a tool to visualize the evolution of pyramid building during the Pyramid Age (2700–1700 BCE). By showing novel visualizations about pyramids, and allowing the user to customize various parameters, it seeks to offer an updated and broader understanding of societal development during this period, addressing the gaps and omissions of past visualizations that have predominantly focused on linear interpretations centered on kings and the structural characteristics of the pyramids. This initiative will generate new charts and infographics for inclusion in an academic publication, providing a comprehensive overview of the development of funerary constructions and their significance through time.

### Goal
- Generate plots related to the status, length of rule, gender (including kings, queens, and other individuals) of pyramid complexes through time and space
- Create updated images based on the ones in `assets/`, which are from 1997. The current images focus exclusively on the pyramids of kings, and they miss other significant developments, such as the expansion of the mortuary temples, areas for decoration, and the evolution of miniature pyramid complexes for queens, among others.
- Combine charts, plots, and information into an infographic that tells a story

### Questions

- How linear is the development of pyramid construction, and to what extent does it reflect the rise and fall of the Pyramid Age?

- How do visual representations, such as those in the `assets/` folder in this repository, influence our perception of these monuments, their development, and the surrounding social context?

## Workflow

### Datasets
The Egyptology team keeps their most up-to-date dataset in a shared Google Drive. Currently, if that dataset is to be retrieved, it will be manually downloaded from Google Drive as a csv file. This constitutes the raw dataset which is found in the ``assets`` directory as ``raw_pyramid_data.csv``. This dataset is formatted in a way that suits the particular organizational needs of the Egyptology team, but it is not in an ideal format for data analysis. Much of the dataset can currently be normalized, but complete "tidiness" cannot yet be achieved, as certain inconsistencies, ambiguities, and potentials for data loss exist while the dataset is in its current form. Therefore, a form of the dataset that has as much normalization as is currently possible can be found in the ``assets`` directory as ``normalized_pyramid_data.csv``, which was created from the raw dataset by way of the cleanup script, which is discussed below.

### Cleanup
The dataset cleanup script can be found in the ``src/cleanup`` directory as ``cleanup_script.py``. An extensive description of the program and its functions can be found in the docstrings written in the script itself. To summarize, it is a script specifically tailored to the typical normalization needs of our Old Kingdom pyramid dataset. Each function can be executed individually either by way of a command-line interface, or by way of a csv file that can be provided to the program in lieu of CLI input. The CLI would be preferable if the user wanted to perform iterative modifications to a dataset, or if they wanted to only perform a small amount of modifications very quicly. The csv file - which lists each desired function and its inputs - would be preferable for performing routine modifications on a dataset that had slight updates, or any other series of modifications that would be too laborious and error-prone to manually type out in the CLI. Irrespective of the precise method, the final, (relatively) normalized dataset should then be stored as ``assets/normalized_pyramid_data.csv``.

### Visual Creation