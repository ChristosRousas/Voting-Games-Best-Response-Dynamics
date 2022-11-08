# Voting-Games-Best-Response-Dynamics
This is an implementation of a learning algorithm (Best Response Dynamics) to find Nash Equilibria for voting games, specifically for the Plurality and Borda voting rules.

It is a simple Python app, so you can run it (for example Plurality, similarly for Borda) on the command prompt in one of 3 ways:
1. `python plurality.py csv game1.csv` to run the algorithm given a csv input of the voters' voting preferences.
2. `python plurality.py random 6 4` to run the algorithm for a random game of e.g. 6 voters and 4 candidates.
3. `python plurality.py test` to test the program for many combinations of the number of voters and candidates and output a csv file of the results.
