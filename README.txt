Competition organised by Google in 2021. The objective is to answer a given 
problem, on the theme of data processing.
The script is made in Python V3. No external library is needed.
The results are calculated and displayed directly in the terminal. The files to
be processed are here(Output).

## Issue(practice_round_2021_v2.pdf)
Isn't it fun to share pizza with friends? But, sometimes you just don't have 
enough time to choose what pizza to order. Wouldn't it be nice if someone else
chose for you?

### Objectives ✔
Help the imaginary pizzeria choose the pizzas to deliver to Hash Code teams.
And since we want everyone to enjoy their food, l et's try to deliver to each
team, as many different ingredients as we can.

### Score Calculation
Even though it’s nice to deliver pizzas to all teams, it is allowed to make
fewer deliveries than the number of teams. However, making more deliveries than
the number of teams is an error. It is also an error to make more deliveries to
2, 3 or 4-person teams than the corresponding number of teams provided in the
input file.

For each delivery, the delivery score i s the s quare of the total number of
different ingredients of all pizzas in the delivery. The total score is the sum
of the scores for all deliveries.

## Solution

### Principle
It is important to have read the instructions for the competition
(practice_round_2021_v2.pdf) beforehand, to understand the rest.

While reading the file, we create our teams and pizzas in the classrooms. Then
we sort them in descending order:
-  The pizzas according to the number of ingredients
-  Teams by number of members

Then a limit of common ingredients is given between the pizza and the team.

#### First step
First 0, 1, 2, ..., maximum possible ingredients.
As soon as a pizza finds a team in the list of available teams, with a number
of ingredients less than or equal to the current limit, it is added to the
team's order list. We move on to the next pizza and start again.
If a team has the maximum number of pizzas possible ordered, it is removed from
the list of available teams. This reduces the number of teams in which you are
looking for a place.

#### Second step
Pizzas that can earn points have been placed.
With the remaining pizzas we put them in the teams where there is still place,
without any other criteria.
Thanks to this, the number of teams with a complete order can be further
increased.

#### Third step
Among the remaining teams that did not complete their order. 
The team with the highest score takes the pizzas from the team with the lowest
score. 
As long as there are still teams that can be complete.

The aim here is to make orders for as many teams as possible. 

### Score(images/Score.png)

This is calculated directly by the script.

File                          | Number of teams | Number of people | Number of pizza | Number of teams delivered | Number of pizza delivered | Score       | Time          |
----------------------------- | --------------- | ---------------- | --------------- | ------------------------- | ------------------------- | ----------- | ------------- |
a_example                     | 4               | 12               | 5               | 1                         | 4                         | 49          | 00h 00min 00s |
b_little_bit_of_everything.in | 185             | 550              | 500             | 160                       | 500                       | 11 017      | 00h 00min 00s |
c_many_ingredients.in         | 1 628           | 4 965            | 10 000          | 1 628                     | 4 965                     | 298 675 358 | 00h 16min 11s |
d_many_pizzas.in              | 8 099           | 25 343           | 100 000         | 8 099                     | 25 343                    | 4 895 657   | 00h 00min 20s |
e_many_teams.in               | 118 775         | 346 409          | 100 000         | 24 999                    | 99 996                    | 10 255 186  | 00h 00min 52s |
Total                         | 128 691         | 377 279          | 210 505         | 34 887                    | 261 614                   | 313 837 267 | 00h 17min 24s |

The calculated score is confirmed by the Judge System of the HashCode
(images/Score_google.png).

### Limits ⚠
-  No unit test
-  At the time of publication, no score comparison is available
-  It resolves quickly but gives an average score 