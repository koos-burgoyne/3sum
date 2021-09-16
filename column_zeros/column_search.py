import numpy as np
import time
from numpy.fft import fft

def threesum(x):
  solution = False
  x = sorted(x)
  for i in range(0,len(x)-2):
    a = x[i]
    start = i + 1
    end = len(x) - 1
    while (start < end):
      b = x[start]
      c = x[end]
      if (a + b + c == 0):
        solution = True
        start = start + 1
        end = end - 1
      elif (a + b + c > 0):
        end -= 1
      else:
        start += 1
  return solution

def new_array(n, min, max):
  a = [0]*n
  a[0] = min
  for i in range(1,n):
    new_val = np.random.randint(a[i-1],a[i-1]+((max-min)/n)*2)
    a[i] = new_val
  return a

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
  key_seq = key_sequence(key_vals)
  #print(key_vals)
  #print(key_seq)
  # check tip values
  last_pair = a[n]*2
  for i in a:
    #action_counter += 1
    if (i+last_pair) == 0:
      solutions.append((i,a[n],a[n]))
  
  # find zeroes
  # iterate triangles
  col_counter = 1
  for i in range(0,n):
    #print(i)
    # iterate columns
    for j in range(col_counter,n):
      
      #print(i,'->',a[i]+a[n-j]+a[n])
      val_to_check = a[i]+a[n-j]+a[n]
      #print('\t',val_to_check)
      if val_to_check == 0:
        #print(a[i],'+',a[n-j],'+',a[n])
        solutions.append((a[i],a[n-j],a[n]))
      elif val_to_check in key_seq:
        if key_seq[val_to_check] < j:
          #print('*',a[i],'+',a[j],'+',a[key_seq[val_to_check]])
          solutions.append((a[i],a[n-j],a[n-key_seq[val_to_check]-1]))

      if j > n-i-1:
        # too far left in columns -> move to next triangle
        break
      if a[i]+a[n-j]+a[n] < key_vals[n-1]:
        # bottom value less than key_vals max -> move to next triangle
        break
    if a[i]+a[n-col_counter]+a[n-col_counter] > 0 or np.abs(a[i]+a[n-col_counter]+a[n-col_counter]) < key_vals[i]:
      col_counter += 1

    # no more columns to check -> end search
    if col_counter > n-i-1:
      break
  
  return solutions

def solve(a):
  print(a)
  print(find_triplets(a))

print()

#a = new_array(10, -18, 20)
#a = [-22, -16, -9, -3, 2, 5, 8, 12, 14, 19]
#solve(a)

min = 200
max = 1001
averages = [0]*(max-min+1)
for i in range(min,max):
  total_tests = 10
  sum_moves = 0
  for j in range(total_tests):
    a = new_array(i, -i*20, i*20)
    start = time.time()
    find_triplets(a)
    end = time.time()
    averages[i-min] += end-start
  averages[i-min] /= total_tests

for i in averages:
  print(i,end=' ')

print()

# Time test against standard algorithm
""" averages = [0]*(max-min+1)
averages_threesum = [0]*(max-min+1)
for i in range(min,max):
  total_tests = 10
  sum_moves = 0
  sum_moves_threesum = 0
  for j in range(total_tests):
    a = new_array(i, -i*20, i*20)
    start = time.time()
    new_num = find_triplets(a)
    end = time.time()
    #print(a,' -> ', new_num)
    averages[i-min] += end-start
    start = time.time()
    new_num_threesum = threesum(a)
    end = time.time()
    averages_threesum[i-min] += end-start
  averages[i-min] /= total_tests
  averages_threesum[i-min] /= total_tests

for i in averages:
  print(i,end=' ')
for i in averages_threesum:
  print(i,end=' ')

print() """