# This module file contains the helper functions needed to perform testing and plot the results
import matplotlib.pyplot as plt
import numpy as np

def new_test_array(n, min, max):
  a = [0]*n
  for i in range(0,int(n/2)):
    new_val = np.random.randint(min,1)
    while new_val in a:
      new_val = np.random.randint(min,1)
    a[i] = new_val
  for i in range(int(n/2), n):
    new_val = np.random.randint(1,max)
    a[i] = new_val
  return a

def grow_test_array(n, germ):
  # base case
  if len(germ) == n:
    return germ
  # create new array
  new_array = [0]*n
  # add new value
  new_array[:len(germ)] = germ
  if n % 2 == 0:
    new_val = np.random.randint(1,10)
    new_array[n - 1] = new_array[n - 3] - new_val
    return new_array
  else:
    new_val = np.random.randint(-10,-1)
    new_array[n - 1] = new_array[n - 3] - new_val
    return new_array

def plot_results(results, min, max, lbl):
  results = np.array(results)
  results[results==0] = np.nan
  plt.plot(np.linspace(min,max,max-min+1), results, "*", label=lbl)