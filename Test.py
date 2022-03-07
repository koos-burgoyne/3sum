import matplotlib.pyplot as plt
import time

from source import Standard
from source import ColumnSearch
from source import Zeroboard
from source import helper


def main():
  min_size = 100
  max_size = 2000
  increment = 200
  num_trials = 1

  a = helper.new_test_array(min_size-1, -min_size*2, min_size*2)

  results_colsearch = [0]*(max_size-min_size+1)
  results_minZB = [0]*(max_size-min_size+1)
  results_threesum = [0]*(max_size-min_size+1)

  for i in range(min_size,max_size,increment):
    print('size:',i)
    sum_time_minZB = 0
    sum_time_col = 0
    sum_time_threesum = 0
    for j in range(0,num_trials):
      a = helper.grow_test_array(i, a)
      b = sorted(a)
      # print('trial:',j+1,end="\r")
      
      start = time.time()
      print(len(ColumnSearch.find_triplets(b)))
      end = time.time()
      sum_time_col += end - start

      start = time.time()
      print(len(Zeroboard.solve(b)))
      end = time.time()
      sum_time_minZB += end - start
      
      start = time.time()
      print(len(Standard.threeSum(b)))
      end = time.time()
      sum_time_threesum += end - start
      
    results_colsearch[i-min_size] = sum_time_col / num_trials
    results_minZB[i-min_size] = sum_time_minZB / num_trials
    results_threesum[i-min_size] = sum_time_threesum / num_trials

  for i in range(len(results_threesum)):
    if results_colsearch[i]!=0:
      print(results_colsearch[i], results_minZB[i], results_threesum[i])

  helper.plot_results(results_colsearch, min_size, max_size, 'Column Search')
  helper.plot_results(results_minZB, min_size, max_size, 'Zeroboard')
  helper.plot_results(results_threesum, min_size, max_size, 'Standard')
  
  plt.xlabel('size of input array')
  plt.ylabel('Runtime (sec)')
  plt.legend()
  plt.show()

if __name__ == "__main__":
  main()