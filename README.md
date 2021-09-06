# Ball Sort
A solver for a ball sorting game.

In particular, this project solves [this game](https://apps.apple.com/us/app/ball-sort-puzzle/id1494648714) in which a player sees a number of urns which are filled with scrambled balls.
There are four balls of each color and two more urns than there are colors; two of the urns are entirely empty to start and the others are filled with a random assortment of the balls.
In order to solve the puzzle, the balls must be moved around until each urn is filled with balls of only one color.
Balls can be moved from the top of an urn to an empty urn or to a different urn that has fewer than four balls already and has a top ball of the same color as the moved ball.

## Usage
For now, configuring the solver requires editing the code in `solve.py` to include the specific configuration that you are trying to solve (or to randomize a puzzle of a certain size).
If you are using new color(s), add their names to the big equality at the top.
Then you can describe a particular layout as a list of lists.
If you want any solution, and not necessarily the most optimal, run the `search` function with `optimal=False`.

Run the solver with
```shell
python3 solve.py
```
or similar. It prints its results as it go
