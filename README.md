# KnowledgeRepresentation

## This repository
This repository contains the files that are necessary to run the SAT Solver. You can find the following files in this repo.
### How to run
The solver can be run by using the terminal of your computer. Navigate to the right directory and type $ python3 SAT.py -h. This command shows the necessary arguments to run this file. Choose what arguments you want and run it again.

### SAT.py
The script that contains the function for solving the sudoku. 
- The first part contains code to run this script in the terminal.
- dpll2(): it contains the general function that contains the solver. It needs no arguments since the necessary variables are global.
- The final parts contains a series of ifelse-statements. This statements make sure the right files and heuristics are used to run the solver.
### dpll2.py
This script contains functions that are used within the dpll2() function in SAT.py
- empty_clause() tests of there is an empty clause.
- tautology() tests if there is a tautology.
- unit_clause() tests if there is a unit clause.
- pure_literal() tests if there is a pure literal.
- remove_lit() removes clauses if they have been satisfied and shortens clauses if the negation of a true literal is present in the clause.
- draw_literal() selects a random literal.
### Heuristics.py
Contains the multiple heuristics for selecting a literal to split on.
### Reading.py and translate_sudokus.py
Contains functions for reading the inputfile.
### Plot_results.py
Contains functions for generating the graphs used in the paper.
