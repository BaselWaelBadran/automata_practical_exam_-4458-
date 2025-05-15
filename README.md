# Theory of Computation Practical Exam

- Name: Basel Wael AbdelMonem Mohamed
- Section: 2

## Overview
This Practical exam contains 3 problems (2 problem to solve are required to pass).
- Problem 1: Write a program that implements a function to convert a regular expression into a DFA and simulate the DFA on a list of input strings.
- Problem 2: Implement a program in Python from scratch (no libraries) that simulates a PDA to determine whether a given input string belongs to this language.
- Problem 3: Write a program that simulates a Turing Machine that recognize the language L={0^n 1^n 0^n 1^n}.

```
Practical/
├──Problem 1
|   ├──reg_to_dfa.py                    # Simpler implementation with hardcoded for RE "(a|b)*abb" 
|   └──reg_to_dfa_v2.py                 # More complex implementation suports (Concatenation, Union, Kleene Star, and Parentheses) for RE with Symbols ('a', 'b').
|
├──Problem 2
|   └──pda_odd_palindrome.py            # Simulating a pushdown automaton (PDA) to check if a string is odd-length palindrome for Symbols ('a', 'b').
|
└──Problem 3
    └──TM.py                            # Simulation of a Turing Machine (TM) to recognize the language L = {0^n 1^n 0^n 1^n}
```


## Usage
Just run the Python files in supported Python environement.