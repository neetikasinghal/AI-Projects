# AI-Projects
Projects done in the Artificial Intelligence Course during Masters at USC

## Placing Police Officers(Using search algorithms)
1. Description: Placing Police Officers to the Blocks having some value(most number of crime activities in that block) such that you address max points such that no 2 officers are on same row & column & diagonal(similar to n queens)
2. Rest of the description can be found under description.pdf under Placing Police Officers folder.
3. hw1cs561f2018.py: Used dfs search technique with recursion similar to nqueens problem and comparing all the nqueen solutions and giving the maximum score. Pruned search space as when queens are equal to number of blocks.


## Serving homeless community(Using game-playing algorithms)
1. Description: Two communities LAHSA(Homeless community), SPLA(Parking LA community) providing bed spaces as well parking spaces for homeless people and optimizing the spaces based on constraints and giving each other alternate turns to choose the best candidate(game playing algorithm)
2. Rest of the description can be found under description.pdf under Serving Homeless community folder.
3. hw2cs561f2018.py: Implemented alternate turn game playing algo which optimizes the best candidate to choose so that bed spaces and parking lots are filled optimally.
4. Sample inputs and their corresponding outputs are given.

## Navigating Autonomous Car(Using Markov Decision Process(MDP))
1. Description: Navigate the autonomous car without getting hit on obstacles and earning maximum money. Each block has a positive value which is basically money and obstacles have losses too. Objective is to drive car along the matrix to get maximum money.
2. Rest of the description can be found under description.pdf under Navigating Autonomous Car folder.
3. hw3cs561f2018.py: Used Policy Iteration as well as Value Iteration to get the best policy and based on that policy simulated the car to move with probabilites of going either in direction according to policy or other directions.
4. Sample input and output are given.