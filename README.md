# Two not touch
Teammembers: Dominic Rogetzer, Johannes Seelig, Carina Heinreichsberger, discussion partner: Andreas Weniger

Two not touch is a sudoku like game, where you have a map with certaina areas, which should be filled with stars, according to specific rules:
* only two stars per row
* only two stars per line
* only two stars per region
* stars are not allowed to touch

Our concept solves the puzzle by making use of quantum computers!

# Introduction
Quantum computers have the possibility to compute things way faster than classical computers by making use of superposition. Some types of problems are particularly suitable for being solved by Quantum computers such as minimizing QUBOs, which we make use of in implementing a solver for the two-not-touch game!

# Basic Principles
A QUBO, short for Quadratic unconstrained binary optimization (https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization) is used to formulate a problem in a mathematical way, so that it can be solved by programs specifically designed for solving such equations . A QUBO combines the objective we have with some constraints, in the form of

	QUBO = min(objective) + gamma * (constraints)

If our objective is, for example, to find the minimum sum of two numbers out of three given numbers {17, 21, 19}, the objective can be formulated by simply: min(17x+21y+19z), where x,y and z are elements of {0,1}.
Additionally we have one constraint, namely that we only want to choose two numbers. Therefor formulate our constraint as x+y+z=2.

Using the Leap IDE respectively the ocean-dwave-sdk, we can make use of the exactsolver, a QUBO solver designed for quantum computers.
The exactsolver takes the QUBO and gives us its minimum, which should be the solution. However sometimes it can happen, that the constraint becomes negative. To prevent this from happening, we have to square the constraint, and multiply it with a factor, so that it can equal out an accidental minimum. Constraint: gamma.(x+y+z-2)^2
When adding the objective and the constraint, we get our QUBO: min(17x+21y+19z)+gamma.(x+y+z-2)^2

This needs to be written in a way, so that the solver can read it, which is a linear combination of our variables. We choose a gamma that is high enough, so that a rule violation won't result in a minimum: gamma = 1000. 

This final QUBO that can be given to our exact solver is: https://latex.codecogs.com/gif.latex?-2985x-2979y-2981z&plus;2000xy&plus;2000xz&plus;2000yz


# Application to our code
Our game has no objective but consists of four constraints, which correspond to the four rules listed in the first section. These four rules need to be formulated in mathematical expressions so that they result in a QUBO. This QUBO will be given to the exact solver, which will solve the puzzle. The result will tell us where on the board we have to put the stars, so that all rules are fulfilled. If a Cell is empty it has the value 0, if it has a star it has the value 1.

Usually this game has a 10x10 Board, but we simplified it to a 4x4 field, with only one star per line/row/area.


1.) One Stars per line
Our first constraint implements the rule, that only one star per line is allowed. This means, that if we add up all the cells in one line, the sum must be 1. This needs to be done for all lines, which results in Constraint 1:
SUM_{j=0}^4 [ SUM_{i=0}^4(x_{i,j})-1]^2 = 0
[Bild](https://latex.codecogs.com/gif.latex?\sum_{j=0}^4&space;\left[&space;\sum_{i=0}^4(x_{i,j})-1&space;\right]^2&space;=&space;0)


2.) One stars per row
Now we are doing the exact same thing as in 1.) Since we are now checking the rows and not the lines, the indices are switch, resulting in:
Constraint 2: SUM_{i=0}^4 [ SUM_{j=0}^4(x_{i,j})-1]^2 = 0
[Bild](https://latex.codecogs.com/gif.latex?\sum_{i=0}^4&space;\left[&space;\sum_{j=0}^4(x_{i,j})-1&space;\right]^2&space;=&space;0)

3.) One stars per region
The regions are given to the code as matrix:



As can be see in the picture above each region has it's own identifier. Here we have four regions. The idea is, that the constraint checks, if there is a star within a region, leading to the formula:
SUM_{k=0}^|R| [(SUM_{(ij) element in R_k} x_{ij}) -1]^2 =0
[Bild](https://latex.codecogs.com/gif.latex?\sum_{k=0}^{|R|}&space;\left[\left(\sum_{(ij)&space;\;\epsilon&space;\;R_k}&space;x_{ij}\right)&space;-1\right]^2&space;=0)

The inner sum checks all cells within a region, allowing only one star to be present. The outer sum traverses all other regions.


4.) Don't touch this ~dumdududum
The idea behind this part is: If x=1 then y=0. This can be formulated as constraint simply by xy=0.
Let's combine this with our problem. If a star is present in a cell, the cell has the value 1, and all surrounding cells need to be 0. If the cell is x_ij, the surrounding cells are x_i-1,j-1, x_i-1, j x_i-1,j+1 .... x_i+1,j-1, x_i+1, j x_i+1,j+1 Therefor we create a Set U_ij of all indices and formulate the constraint:

constraint 4: SUM_ij (SUM_{r_0 element U_{ij}} x_{ij} x_{r_0})
[Bild](https://latex.codecogs.com/gif.latex?\sum_{ij}&space;\sum_{r_0&space;\;&space;\epsilon\;&space;U_{ij}}&space;x_{ij}&space;x_{r_0})


5.) QUBO
Thanks to the linearity of the QUBO we can simply add all our constraints. Since writing this down by hand will result in pages of calculations, we coded a solver, that takes the sums and vereinfacht it to a linearcombination, which we can then give to the exactsolver. 

# Testrun


# ToDO / Troubles
Sadly our time ran out befor we could fix all errors. Currently our program is killed when computed in Leap IDE. This is the major thing we would love to fix if we had more time. 

Other things we wanted to implement:
* input/ output file
* 10x10 boards
* nicer design with grafic output
