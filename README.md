# Theory of Computation Practical Exam

Name: Basel Wael AbdelMone Mohamed
Section: 2

## Overview
This Practical exam contains 3 problems (2 problem to solve are required to pass).
- Problem 1: Write a program that implements a function to convert a regular expression into a DFA and simulate the DFA on a list of input strings.
- Problem 2: Implement a program in Python from scratch (no libraries) that simulates a PDA to determine whether a given input string belongs to this language.


Practical/
```
├──Problem 1
    ├──reg_to_dfa.py                    # Simpler implementation with hardcoded for RE "(a|b)*abb" 
    └──reg_to_dfa_v2.py                 # More complex implementation suports (Concatenation, Union, Kleene Star, and Parentheses) for RE with Symbols ('a', 'b').
├──Problem 2
    └──pda_odd_palindrome.py            # Simulating a pushdown automaton (PDA) to check if a string is odd-length palindrome for Symbols ('a', 'b').
```


## Usage
Just run the Python files in supported Python environement.