# Oral formulaic poetry

An analysis tool to compare different measures over parallel corpora of Slavic texts; conditional entropy (CE), 
the type-token relationship (TTR), word unigram (UG) and bigram (BG) as a measure of predictability.

## Installation

1. Clone the code from oral-formulaic-poetry [git](https://github.com/ncsa-mo/oral-formulaic-poetry.git) repository in your local folder.
2. Install required Python packages. Currently `numpy`, a package for scientific computing and `pandas`, a package for data analysis tools.
3. We recommend using virtual environment, [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (preferred) for python 3.7+. for managing Python environments. Create the environment from the terminal at the project 
folder (called `ofp` here) and activate it:

   ```
   conda create -n ofp python=3.8
   source activate ofp
   ```
    
4. From the terminal at the project folder install required packages. Use `conda` for installing packages:

   ```
   conda install numpy
   conda install pandas
   ```

## Running

Run from oral-formulaic-poetry folder (master branch): 
   
   ```
   git branch -a git checkout master
   ```
and
   ```
   python3 measures.py
   (python3 <path_to_oral_formulaic_poetry>/oral-formulaic-poetry/ofp/conditional_entropy/measures.py)
   ```
      
## Testing
