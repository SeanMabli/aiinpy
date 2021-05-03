import numpy as np
import aiinpy as ai
import wandb

wandb.init(project='rnn')

PositiveComments = open("C:\\Users\\smdro\\Downloads\\archive\\sentence_polarity\\rt-polarity.pos", "r")
NegativeComments = open("C:\\Users\\smdro\\Downloads\\archive\\sentence_polarity\\rt-polarity.neg", "r")
Comments = str(PositiveComments.read() + NegativeComments.read())
Comments = np.array(Comments.splitlines())

UniqueWords = list(set([w for Sentence in Comments for w in Sentence.split(' ')]))
Rnn = ai.RNN(8, 2, "ManyToOne")

def WordToBinary(Input):
  Dec = list(bytearray(Input, "utf8"))
  Output = [''] * len(Input)
  for i in range(len(Input)):
    Output[i] = bin(Dec[i]).replace("b", ("0"*(9-len(bin(Dec[i])))))
  return Output

for Generation in range(100000):
  Random = np.random.randint(0, len(Comments))

  t = WordToBinary(Comments[Random])
  print(t)
  Input = np.zeros((len(t), 8))
  for i in range(len(t)):
    Input[i, :] = np.array(list(t[i]))

  Output = Rnn.ForwardProp(Input)

  RealOutput = np.array([1, 0]) if Random < 5331 else np.array([0, 1])

  OutputError = RealOutput - Output

  Rnn.BackProp(OutputError)
  wandb.log({"Error": np.sum(np.abs(OutputError))})