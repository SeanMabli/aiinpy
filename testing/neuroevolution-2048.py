import numpy as np
import testsrc as ai
import wandb
from alive_progress import alive_bar

wandb.init(project="2048")

PopulationSize = 1000

model = ai.neuroevolution((4, 4), 4, PopulationSize, [
  ai.nn((4, 4), 16, ai.sigmoid(), 0.1),
  ai.nn(16, 4, ai.stablesoftmax(), 0.1)
])

Alive = np.array([True] * PopulationSize, dtype=bool)
Score = np.zeros(PopulationSize, dtype=int)

Board = np.ones((4, 4), dtype=int)
PreviousBoard = np.ones((4, 4), dtype=int)

def NewRandom(Num):
  global Board
  for _ in range(Num):
    if 1 in Board:
      Random = np.random.randint(0, 4, 2)
      while Board[Random[0], Random[1]] != 1:
        Random = np.random.randint(0, 4, 2)
      Board[Random[0], Random[1]] = np.random.choice([2, 4], p=[0.9, 0.1])

NewRandom(2)

NumOfGenerations = 1000

with alive_bar(NumOfGenerations) as bar:
  for Generation in range(NumOfGenerations):
    for Player in range(PopulationSize):
      while Alive[Player]:
        Out = model.forwardsingle(np.log2(Board) / 11, Player)

        if np.max(Out) == Out[0]:
          PreviousBoard[:, :] = Board[:, :].copy()
          for _ in range(3):
            for i in reversed(range(3)):
              for j in range(4):
                if Board[i, j] == Board[i + 1, j]:
                  Board[i, j] *= 2
                  Board[i + 1, j] = 1
                if Board[i, j] == 1:
                  Board[i, j] = Board[i + 1, j]
                  Board[i + 1, j] = 1
                  
          NewRandom(1)

        if np.max(Out) == Out[1]:
          PreviousBoard[:, :] = Board[:, :].copy()
          for _ in range(3):
            for i in range(4):
              for j in range(1, 4):
                if Board[i, j] == Board[i, j - 1]:
                  Board[i, j] *= 2
                  Board[i, j - 1] = 1
                if Board[i, j] == 1:
                  Board[i, j] = Board[i, j - 1]
                  Board[i, j - 1] = 1

          NewRandom(1)

        if np.max(Out) == Out[2]:
          PreviousBoard[:, :] = Board[:, :].copy()
          for _ in range(3):
            for i in range(1, 4):
              for j in range(4):
                if Board[i, j] == Board[i - 1, j]:
                  Board[i, j] *= 2
                  Board[i - 1, j] = 1
                if Board[i, j] == 1:
                  Board[i, j] = Board[i - 1, j]
                  Board[i - 1, j] = 1

          NewRandom(1)

        if np.max(Out) == Out[3]:
          PreviousBoard[:, :] = Board[:, :].copy()
          for _ in range(3):
            for i in range(4):
              for j in reversed(range(3)):
                if Board[i, j] == Board[i, j + 1]:
                  Board[i, j] *= 2
                  Board[i, j + 1] = 1
                if Board[i, j] == 1:
                  Board[i, j] = Board[i, j + 1]
                  Board[i, j + 1] = 1

          NewRandom(1)

        Score[Player] = np.sum(Board[:, :])

        if np.array_equal(PreviousBoard[:, :], Board[:, :]):
          Alive[Player] = False

      Board = np.ones((4, 4), dtype=int)
      PreviousBoard = np.ones((4, 4), dtype=int)

    if Generation % 10 == 0:
      for Player in range(PopulationSize):
        if Score[Player] == np.max(Score):
          model.mutate(Player)
          break

      wandb.log({"Score": np.max(Score)})

      Score = np.zeros(PopulationSize, dtype=int)

    bar()
    Alive = np.array([True] * PopulationSize, dtype=bool)
