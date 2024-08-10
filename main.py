import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, Iterable
from operator import attrgetter
from functools import partial
from dataclasses import dataclass
import csv

FILENAME: str = "DS0004.CSV"

def load_csv(filename: str) -> list[str]:
  with open(filename) as samples:
    reader = csv.reader(samples, delimiter=",")
    lines = [r[0:-1] for r in reader]
    return lines

def is_convertible(data, convertion_fun: Callable) -> bool:
  try: convertion_fun(data)
  except ValueError: return False
  else: return True

is_float = partial(is_convertible, convertion_fun=float)

def create_filter(filter_fun: Callable) -> Callable[[Iterable], Iterable]:
  """
  Works under the assumption that the first field can
  be used as a signature of the row's type
  """
  return lambda data: filter(
    lambda d: filter_fun(d[0]) and len(d) > 1,
    data
  )

filter_floats = create_filter(is_float)
filter_non_floats = create_filter(lambda x: not(is_float(x)))

@dataclass(frozen=True)
class Sample:
  time: float
  value: float


def main() -> None:
  data = load_csv(FILENAME)
  header = dict(
    map(
      lambda s: (s[0], float(s[1]) if is_float(s[1]) else str(s[1])),
      filter_non_floats(data) 
    )
  )

  samples = [*map(
    lambda s: Sample(float(s[0]), float(s[1])),
    filter_floats(data) 
  )]

  times = np.array(
    list(
      map(attrgetter('time'), samples)
    )
  )
  values = np.array(
    list(
      map(attrgetter('value'), samples)
    )
  ) * header['Vertical Scale']

  plt.plot(times, values)
  plt.grid()
  plt.show()

if __name__ == "__main__":
  main()