# Oral formulaic poetry

An analysis tool to compare different measures over parallel corpora of Slavic texts; conditional entropy (CE), 
the type-token relationship (TTR), word unigram (UG) and bigram (BG) as a measure of predictability.

## Installation

1. Clone the code from oral-formulaic-poetry [git](https://github.com/ncsa-mo/oral-formulaic-poetry.git) repository in your local folder.
2. Install required Python packages. Currently `numpy`, a package for scientific computing, `pandas`, a package for data analysis tools, and a testing package `pytest`.
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
   conda install pytest
   ```

## Running

Run from `oral-formulaic-poetry` folder (master branch):
   ```
   python3 -m conditional_entropy.measures
   ```
Note that with `-m` command-line flag Python will import a `conditional_entropy` module, then run it as a script which executes the `__main__` with the relative imports working correctly.
      
The `rukopisy_data_formatted.csv` is saved in results folder. A user can compare it with our final values stored in `rukopisy_data_formatted_fin.csv` file in `tests` folder.

## Testing

A user can use `pytest` for comparison of calculated and template, our final files. 
In terminal change directory from your in your `oral-formulaic-poetry` local folder to `test` and run command:
   ```
   pytest test_ofc.py --no-header --no-summary
   ```
The test should pass if values AND file formatting are identical.
