import numpy as np
import random
import math
from functools import reduce
from operator import mul
from decimal import Decimal
from collections import namedtuple, Counter, deque, defaultdict, OrderedDict
import string
import re
from itertools import islice, combinations, permutations
import itertools
from bisect import insort
import sys
import regex
from time import time


def dice(minimum, maximum):
    seed = int(time())
    ma = seed % maximum if maximum != 0 else 0
    mi = seed % minimum if minimum != 0 else 0
    return 333

print(dice(0, 2))
print("hi")