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
  for i in range(int(n/2)):
    new_val = np.random.randint(min,0)
    while new_val in a:
      new_val = np.random.randint(min,0)
    a[i] = new_val
  for i in range(int(n/2), n):
    new_val = np.random.randint(0,max)
    while new_val in a:
      new_val = np.random.randint(0,max)
    a[i] = new_val
  return a

def grow_test_array(n, min, max, germ):
  # base case
  if len(germ) == n:
    return germ
  # create new array
  new_array = [0]*n
  # add - to left or + to right
  if n % 2 == 0:
    new_array[:len(germ)] = germ
    new_val = np.random.randint(1,3)
    """ while new_val in new_array:
      new_val = np.random.randint(1,3) """
    new_array[n - 1] = new_array[n - 2] - new_val
    return new_array
  else:
    new_array[1:n] = germ
    new_val = np.random.randint(-3,-1)
    """ while new_val in new_array:
      new_val = np.random.randint(min,0) """
    new_array[0] = new_array[1] - new_val
    return new_array

def binary(x):    # must put into an array that goes from 0 to max_val in order to convolve properly 
  min_x = min(x)
  z = [0]*(max(x) + 1)
  for i in x:
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

def find_zeros(a):
  # convert a to binary for convolution
  a_bin = binary(a)
  # convolve the binary of a with itself: this is the cartesian sum
  result = fft_convolve(a_bin)
  #a_convolved = [ int(np.round(np.real(x))) for x in result]

  # store max index for solutions array
  max_idx = len(result) - 1
  solution = False

  for i in a:
    index_to_check = max_idx - (i + a[1]*2)
    if index_to_check <= max_idx and i*3 < 0:
      if int(np.round(np.real(result[index_to_check]))) != 0:
        solution = True
  
  return solution

def find_zeros_timed(a):
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

  # store max index for solutions array
  max_idx = len(result) - 1
  solution = False

  start= time()
  for i in a:
    index_to_check = max_idx - (i + a[1]*2)
    if index_to_check <= max_idx and i*3 < 0:
      if int(np.round(np.real(result[index_to_check]))) != 0:
        solution = True
  end = time()
  print(str(end-start))

  return solution

print('\n*** Time test for 3 Sum Algorithm ***')

# test on individual array
# set individual test paremters
array_size = 1000
ratio = 1.1
max_val = array_size*ratio
min_val = -max_val
print('Creating new test array...')
#a = [-628, -65, -455, -46, -281, -67, -552, -104, -537, -103, -590, -268, -490, -109, -493, -568, -472, -370, -56, -528, -274, -335, -410, -435, -185, -257, -505, -133, -464, -344, -129, -57, -165, -228, -320, -154, -134, -88, -14, -398, -424, -183, -76, -180, -200, -392, -350, -359, -291, -105, -214, -280, -327, -333, -94, -321, -127, -232, -255, -59, -238, -249, -292, -192, -27, -261, -42, -143, -216, -107, -258, -6, -248, -28, -38, -102, -126, -210, -101, -77, -121, -130, -100, -20, -136, -51, -11, -87, -44, -137, -39, -95, -96, -113, -89, -15, -3, -66, -1, -16, -72, -45, -61, -13, -40, -17, -32, -18, -12, -7, -4, -8, -5, -2, 3, 9, 7, 4, 10, 8, 41, 27, 22, 30, 45, 44, 60, 2, 31, 16, 43, 18, 71, 68, 74, 24, 77, 101, 38, 23, 115, 159, 165, 172, 28, 183, 17, 5, 94, 109, 197, 208, 133, 125, 161, 140, 87, 218, 47, 236, 122, 81, 49, 12, 266, 257, 82, 310, 130, 278, 91, 309, 97, 99, 238, 164, 262, 318, 62, 194, 200, 78, 405, 277, 351, 342, 367, 414, 365, 73, 65, 154, 449, 167, 152, 383, 408, 206, 93, 169, 215, 33, 96, 392, 291, 360, 202, 315, 123, 397, 486, 274, 121, 269, 331, 104, 317, 522, 316, 204, 221, 119, 461, 241, 534, 55, 470]
a = new_test_array(array_size, min_val, max_val)
print('New array complete')
#print(a)
#print('For array of size', array_size, 'with values in range', min_val, '->', max_val, ':')
# perform test
min_time = 10
max_time = 0
sum_times = 0
total_tests = 1
for i in range(total_tests):
  #print(i)
  start = time()
  #find_zeros(a)
  end = time()
  #print(end - start,'seconds')
  if (end - start) > max_time:
    max_time = (end - start)
  if (end - start) < min_time:
    min_time = (end - start)
  sum_times += (end - start)
print('min:', min_time)
print('max:', max_time)
print('mean:', sum_times / total_tests)

""" 
# set test paremters
n = 500
ratio = 1

# compute test stats for parameters
min_size = 700
max_size = 2000
# starting array
#a = [-630,-627,400]

f = open("3sum_results_means.csv","w")

for _range in range(min_size, max_size + 1):
  print(_range, end=',')
  a = new_test_array(500, -_range, _range)
  # perform test
  min_time = 10
  max_time = 0
  sum_times = 0
  total_tests = 10
  for i in range(total_tests):
    start = time()
    find_zeros(a)
    end = time()
    # capture test time
    if (end - start) > max_time:
      max_time = (end - start)
    if (end - start) < min_time:
      min_time = (end - start)
    sum_times += (end - start)
  # write test summary
  result = str(_range) + ',' + str(min_time) + ',' + str(max_time) + ',' + str(sum_times/total_tests) + "\n"
  f.write(result)
  #if end - start > 0.01:
  #print(a)
print

f.close() """