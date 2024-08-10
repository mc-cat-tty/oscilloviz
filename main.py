import matplotlib.pyplot as plt
import numpy as np
from typing import Callable
from operator import itemgetter
import csv

FILENAME: str = "DS0004.CSV"

def load_csv(filename: str) -> list[str]:
  with open(filename) as samples:
    reader = csv.reader(samples, delimiter=",")
    lines = [r[0:-1] for r in reader]
    return lines

def create_data_reader(filename) -> Callable:
  return load_csv(filename)

def is_float(data) -> bool:
  try: float(data)
  except ValueError: return False
  else: return True

def main() -> None:
  data = load_csv(FILENAME)
  header = tuple(row for row in data if not is_float(row[0]))
  samples = tuple(
    tuple(map(float, row))
    for row in data if is_float(row[0])
  )
  times = np.array(
    list(
      map(itemgetter(0), samples)
    )
  )
  values = np.array(
    list(
      map(itemgetter(1), samples)
    )
  )

  plt.plot(times, values)
  plt.grid()
  plt.show()

if __name__ == "__main__":
  main()