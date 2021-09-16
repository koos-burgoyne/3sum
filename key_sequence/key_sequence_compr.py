import numpy as np
from numpy.fft import fft, ifft
from time import time

def naive_sum(a):
  solution = False
  for x in a:
    for y in a:
      for z in a:
        if (x+y+z) == 0:
          solution = True
  return solution          

def new_test_array(n, min, max):
  a = [0]*n
  for i in xrange(n/2):
    new_val = np.random.randint(min,0)
    while new_val in a:
      new_val = np.random.randint(min,0)
    a[i] = new_val
  for i in xrange(n/2, n):
    new_val = np.random.randint(0,max)
    while new_val in a:
      new_val = np.random.randint(0,max)
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
    new_val = np.random.randint(1,3)
    new_array[n - 1] = new_array[n - 3] - new_val
    return new_array
  else:
    new_val = np.random.randint(-3,-1)
    new_array[n - 1] = new_array[n - 3] - new_val
    return new_array

def key_values(x):
  values = []
  for i in range(len(x)-1,0,-1):
    values.append(x[i]-x[i-1])
  return values

def key_sequence(x):
  values = [0]
  for i in range(len(x)-1,0,-1):
    values.append(values[len(values)-1] + x[i]-x[i-1])
  return values

def binary(x, compression_ratio):
  key_seq = key_sequence(x)
  print(key_seq)
  if compression_ratio > 1:
    for i in range(len(key_seq)):
      key_seq[i] = int(key_seq[i]/compression_ratio)
  print(key_seq)
  max_val = max(key_seq)
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

def find_zeros(a):
  # convert a to binary for convolution
  key_vals = key_values(a)
  compression_ratio = min(key_vals)
  a_bin = binary(a, compression_ratio)

  solution_set = fft_convolve(a_bin)

  solution = False
  last_pair = a[len(a)-1]*2
  for i in range(len(a)-1):
    index_to_check = a[i] + last_pair
    if (a[i]*3 < 0) and int(int(np.round(np.real(solution_set[index_to_check])))/compression_ratio) != 0:
      print(index_to_check, end=' ')
      print(a[i]*3, end='; ')
      solution = True
  return solution

print()

a = [-12, -10, -7, 1, 3, 8]
print(find_zeros(a))

print()