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
The most up-to-date dataset in a shared folder on Google Drive. Currently, if that dataset is to be retrieved, it will be manually downloaded from that location as a csv file. This constitutes the raw dataset which is found in the `assets` directory as `raw_pyramid_data.csv`. This version of the dataset is formatted in a way that suits some particular organizational workflows, but it is not in an ideal format for data analysis. A more analysis-ready version of the dataset can be found in `assets/normalized_pyramid_data.csv`, which was created from the raw dataset by way of the cleanup script (see [here](#cleanup)).

### Package Management

#### Installation

This project makes use of Poetry for package management. In order to install a compatible version of Poetry, Python version 3.9 or greater must be installed on your system. Poetry can be installed by following the instructions on [its official website](https://python-poetry.org/docs/#installation).

To resolve the project's dependencies, navigate to the top level of the directory and run

`poetry install`

#### Running files

Once complete, cells in Jupyter notebooks can be run within a given notebook without using Poetry. However, the scripts used to generate completed visuals will require poetry in order to run properly. To run a script, run

`poetry run python path/to/script`

or

`poetry run python3 path/to/script`

depending on how your system refers to your Python version in its `PATH`.

#### Adding new dependencies

When a new dependency is added to the project, it can be added to Poetry by way of `pyproject.toml` by running

`poetry add name-of-dependency`

### Cleanup
The dataset cleanup script can be found in the `src/cleanup/cleanup_script.py` file. An extensive description of the program and its functions can be found in the docstrings written in the script itself. To summarize, it is a script specifically tailored to the typical normalization needs of our Old Kingdom pyramid dataset. Each function can be executed individually either by way of a command-line interface, or by way of a csv file that can be provided to the program in lieu of CLI input. The CLI would be preferable if the user wanted to perform iterative modifications to a dataset, or if they wanted to only perform a few minor modifications quickly. The csv file - which lists each desired function and its inputs - would be preferable for performing routine modifications on a new version of the dataset that had minor updates, or any other series of modifications that would be too laborious and error-prone to manually type out in the CLI. Irrespective of the selected approach, the final, (relatively) normalized dataset should then be stored as `assets/normalized_pyramid_data.csv`.

### Visual Prototyping
We experiment with the creation of various different types of visuals in Jupyter notebooks, which can be stored in the ``Notebooks`` directory. Dynamic visuals can and have been created with Plotly, but as of the time of writing we have decided to put those on hold for now. If one would like to create or edit new or existing visuals of that type, they can be created with reference to the Plotly.js template that exists under the `templates` directory, which will create a webpage that can be stored in the `docs` directory. This allows for the webpage to be hosted through GitHub Pages for public viewing purposes, which is performed automatically so long as the webpage is stored in the `docs` directory.

### Visual Scripts
When a given visual is selected and is in a near-complete state, it should be moved from its respective notebook into a dedicated script/file. Such scripts can be found in the `src` directory, either under ``src/plots``, or under a presently undetermined directory for non-plot visuals, which may possibly include dynamic visuals or infographics. The output of plot scripts should generally take the format of PNG images, which are to be stored in the `images` directory.