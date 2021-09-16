import numpy as np
import time
from numpy.fft import fft

def new_test_array(n, min, max):
  a = [0]*n
  for i in range(0,int(n/2)):
    new_val = np.random.randint(min,1)
    """ while new_val in a:
      new_val = np.random.randint(min,0) """
    a[i] = new_val
  for i in range(int(n/2), n):
    new_val = np.random.randint(1,max)
    """ while new_val in a:
      new_val = np.random.randint(0,max) """
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

def key_sequence(x):
  sequence = {}
  prev = 0
  for i in range(len(x),0,-1):
    sequence[prev + x[i-1]] = len(x)-i
    prev += x[i-1]
  return sequence

def find_triplets(a):
  solutions = []
  n = len(a)-1
  # create key sequence
  key_vals = [ a[i]-a[i-1] for i in range(1,n+1) ]
  key_seq = {}
  prev = 0
  for i in range(n,0,-1):
    key_seq[prev + key_vals[i-1]] = n-i
    prev += key_vals[i-1]
  # find zeroes
  col_counter = 1
  for i in range(0,n):
    #print(i)
    # iterate columns
    for j in range(col_counter,n):
      val_to_check = a[i]+a[n-j]+a[n]
      if val_to_check == 0:
        solutions.append((a[i],a[n-j],a[n]))
      elif val_to_check in key_seq:
        if key_seq[val_to_check] < j:
          solutions.append((a[i],a[n-j],a[n-key_seq[val_to_check]-1]))
      # too far left in columns -> move to next triangle
      if j > n-i-1:
        break
      # bottom value less than key_vals max -> move to next triangle
      if a[i]+a[n-j]+a[n] < key_vals[n-1]:
        break
    if a[i]+a[n-col_counter]+a[n-col_counter] > 0 or np.abs(a[i]+a[n-col_counter]+a[n-col_counter]) < key_vals[i]:
      col_counter += 1
    # no more columns to check -> end search
    if col_counter > n-i-1:
      break
  return solutions

def solve(x):
  n = len(x)-1
  a = []
  
  # get first column to include in zeroBoard: time < N
  start_col = 0
  while (x[start_col]+x[start_col]+x[n]) < 0:
    start_col += 1

  # get last column to include in zeroBoard: time < N
  end_col = start_col
  while (x[0]+x[end_col]+x[end_col]) < 0 and end_col < (n):
    end_col += 1
  if end_col != n: end_col -= 1
  #print(start_col, end_col)

  zeroboard_size = end_col-start_col+1

  # create key sequence to get zeroBoard column heights: time < N
  key_seq = {}
  prev = 0
  for i in range(n-1,-1,-1):
    key_seq[-(prev + x[i] - x[i+1])] = i + 1
    prev += (x[i] - x[i+1])  
  #print('key_seq\t:',key_seq)
  
  # store edge margins: time < N
  top_edges = [0]*(zeroboard_size)
  bottom_edges = [0]*zeroboard_size
  for i in range(start_col,end_col+1):
    if i == start_col: top = 0
    else:
      top = top_edges[i-start_col-1]
      while (x[start_col]+x[i]+x[n-top]) >= 0 and n-top > i:
        #print(x[start_col]+x[i]+x[n-top],n-top,i)
        top += 1
    top_edges[i-start_col] = top

    if i == start_col: bottom = 0
    else:
      bottom = bottom_edges[i-start_col-1]
      while x[0]+x[i]+x[n-bottom] < 0 and bottom > 0:
        bottom -= 1
    bottom_edges[i-start_col] = bottom

  # add columns to zeroboard: time UNKNOWN
  zbSize = 0
  zeroboard_tip = x[0]+x[n]+x[n]
  zeroboard = {}
  for i in range(0, zeroboard_size):
    start = i + start_col
    for j in range(0, top_edges[i]-bottom_edges[i]+1):
      zbSize += 1
      #print(zeroboard_tip - (x[0]+x[start]+x[n-(j+bottom_edges[i])]))
      insertion_value = zeroboard_tip - (x[0]+x[start]+x[n-(j+bottom_edges[i])])
      if insertion_value not in zeroboard:
        zeroboard[insertion_value] = [[x[start], x[n-(j+bottom_edges[i])]]]
      else:
        zeroboard[insertion_value].append([x[start], x[n-(j+bottom_edges[i])]])
  #print('zBoard\t:',zeroboard)
  #print(len(x),',',zbSize)
  # get check range: time < 2N (for first_check_val, can I use key_seq Dictionary for constant time?)
  final_pair = x[n]+x[n]
  first_check_val = 0
  while (x[first_check_val]+final_pair) < 0:
    first_check_val += 1
  last_check_val = start_col
  while (x[last_check_val]+x[last_check_val]+x[last_check_val]) < 0:
    last_check_val += 1
  
  # check zeroboard for zeros: time < N*(width of zeroBoard at a maximum) -> find the max possible width of a zeroboard in relation to N and we have a runtime
  solutions = []
  for i in range(first_check_val,last_check_val):
    val_to_check = x[i] + final_pair
    if val_to_check in zeroboard:
      for pairs in zeroboard[val_to_check]:
        pairs.append(x[i])
        solutions.append(pairs)
  
  return solutions

def threeSum(nums):
  n=len(nums)
  result = []
  for i in range(0,n-2):
    a = nums[i]
    start = i+1
    end = n-1
    while (start<end):
      b = nums[start]
      c= nums[end]
      if (a+b+c) == 0:
        result.append([a,b,c])
        start += 1
        end -= 1
      elif (a+b+c) > 0:
        end -= 1
      else:
        start += 1
  return result

min_size = 64000
max_size = min_size+1
num_trials = 3

a = new_test_array(min_size-1, -min_size*2, min_size*2)

results_colsearch = [0]*(max_size-min_size+1)
#results_minZB = [0]*(max_size-min_size+1)
results_threesum = [0]*(max_size-min_size+1)

for i in range(min_size,max_size):
  #sum_time_minZB = 0
  sum_time_col = 0
  sum_time_threesum = 0
  for j in range(0,num_trials):
    #a = grow_test_array(i, a)
    b = sorted(a)
    #print(b)
    
    """ start = time.time()
    solve(b)
    end = time.time()
    sum_time_minZB += end - start """

    start = time.time()
    find_triplets(b)
    end = time.time()
    sum_time_col += end - start

    start = time.time()
    threeSum(b)
    end = time.time()
    sum_time_threesum += end - start

  results_colsearch[i-min_size] = sum_time_col / num_trials
  #results_minZB[i-min_size] = sum_time_minZB / num_trials
  results_threesum[i-min_size] = sum_time_threesum / num_trials

for i in range(0,max_size-min_size+1):
  print(results_colsearch[i],results_threesum[i])

# individual tests
#input_set = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
#input_set = [-20, -18, -15, -12, -8, -5, -2, -1, 4, 6]   # [[6, 6, -12], [4, 4, -8], [-1, 6, -5], [-2, 4, -2]]
#input_set = [-40, -34, -21, -12, -1, 12, 16, 22, 35, 48] # [[-1, 35, -34], [12, 22, -34], [-1, 22, -21]]

#solutions = solve(input_set)
#print(solutions)
