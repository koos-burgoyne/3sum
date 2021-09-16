import numpy as np
from numpy.fft import fft, ifft
import time

def naive_sum(a):
  solution = False
  for x in a:
    for y in a:
      for z in a:
        if (x+y+z) == 0:
          solution = True
  return solution          

def new_array(n, min, max):
  a = [0]*n
  a[0] = min
  for i in range(1,n):
    new_val = np.random.randint(a[i-1]+1,a[i-1]+((max-min)/n)*2)
    while new_val == 0:
      new_val = np.random.randint(a[i-1]+1,a[i-1]+((max-min)/n)*2)
    a[i] = new_val
  return a

def key_sequence(x):
  values = {0:0}
  n = len(x)
  prev = 0
  for i in range(len(x)-1,0,-1):
    values[prev + x[i]-x[i-1]] = n-i
    prev += x[i]-x[i-1]
  return values

def binary(x, key_seq):
  max_val = 0
  for val in key_seq:
    if val > max_val:
      max_val = val
  z = [0]*(max_val+1)
  for i in key_seq:
    z[i] = 1
  return z

def fft_convolve(x):
  N = len(x)
  zero_pad_x = np.zeros(2*N)
  zero_pad_x[0:len(x)] = x
  fft_zero_pad_x = fft(zero_pad_x)
  # Multiply element-wise:
  fft_zero_pad_x *= fft_zero_pad_x
  # Conjugate element wise:
  result = np.conj(fft_zero_pad_x)
  result = fft(result)
  result /= float(2*N)
  return result[:2*N-1]

def find_zeros_timed(a):
  # find max
  start = time()
  
  end = time()
  print(str(end-start),end=',')

  # convert a to binary for convolution
  start = time()
  a_bin = binary(a)
  end = time()
  print(str(end-start),end=',')

  start = time()
  # convolve the binary of a with itself: this is the cartesian sum
  result = fft_convolve(a_bin)
  end = time()
  print(str(end-start),end=',')

  """ start = time()
  a_convolved = [ int(np.round(np.real(x))) for x in result]
  end = time()
  print(str(end-start),end=',') """
  
  # store max index for solutions array
  max_idx = len(result) - 1
  solution = False

  start= time()
  for i in a:
    index_to_check = max_idx - (i + a[1]*2)
    if index_to_check <= max_idx and i*3 < 0:
      if int(np.round(np.real(x)))(result[index_to_check]) != 0:
        solution = True
  end = time()
  print(str(end-start))

  return solution

def find_zeros(a, key_seq):
  # convert a to binary for convolution
  a_bin = binary(a, key_seq)
  # create solution set
  solution_set = fft_convolve(a_bin)
  # query for solutions using tip values
  zeros = []
  last_pair = a[len(a)-1]*2
  for i in range(len(a)-1):
    if a[i]*3 > 0:
      break
    index_to_check = a[i] + last_pair
    if int(np.round(np.real(solution_set[index_to_check]))) != 0:
      zeros.append(i)
  return zeros

def find_solutions(a):
  if np.max(a) <= 0:
    return []
  solutions = []
  key_seq = key_sequence(a)
  zeros = find_zeros(a, key_seq)
  n = len(a)-1
  
  # check tip values
  last_pair = a[n]*2
  for i in a:
    if (i+last_pair) == 0:
      solutions.append((i,a[n],a[n]))
  
  # find zeroes
  # iterate triangles
  inter_col_counter = 1
  col_counter = 1
  for i in zeros:
    # iterate columns
    # while column top is + mov counter back
    while a[i]+a[n-inter_col_counter]+a[n-inter_col_counter] > 0:
      inter_col_counter += 1
    col_counter = inter_col_counter
    # while column bottom is + move next counter back
    while a[i]+a[n]+a[n-col_counter] >= 0 and col_counter <= (n-i):
      key_to_check = a[i]+a[n]+a[n-col_counter]
      if key_to_check in key_seq:
        solutions.append((a[i],a[n-col_counter],a[n-key_seq[key_to_check]]))
      col_counter += 1

    # no more columns to check -> end search
    if inter_col_counter > n-i-1:
      break
  
  return solutions

print()

min = 10
max = 501
averages = [0]*(max-min+1)
for i in range(min,max):
  total_tests = 5
  sum_moves = 0
  for j in range(total_tests):
    a = new_array(i, -i*2, i*2)
    start = time.time()
    find_solutions(a)
    end = time.time()
    averages[i-min] += end-start
  averages[i-min] /= total_tests

for i in averages:
  print(i)

""" a = [-20, -17, -14, -13, -10, -5, -2, 5, 9, 15]
print(find_solutions(a)) """

print()