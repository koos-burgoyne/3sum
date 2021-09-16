import numpy as np
from numpy.fft import fft, ifft
from time import time

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
  """ for i in fft_zero_pad_x:
    print(i, end=' ')
  print('\n\n') """
  for i in fft_zero_pad_x:
    print(np.abs(int(np.round(np.real(i)))), end=' ')
  print()
  for i in fft_zero_pad_x:
    print(np.abs(int(np.round(np.imag(i)))), end=' ')
  print()
  fft_zero_pad_x *= fft_zero_pad_x
  """ for i in fft_zero_pad_x:
    print(int(np.round(np.real(i))), end=' ')
  print() """
  # Conjugate element wise:
  result = np.conj(fft_zero_pad_x)
  result = fft(result)
  for i in result[:2*N-1]:
    print(int(np.round(np.real(i))), end=' ')
  print()
  #result /= float(2*N)
  return result[:2*N-1]


b = [1,3,5,6,8]
print(fft_convolve(b))
b = binary(b)

for i in b:
  print(i, end=' ')
print()

b = fft_convolve(b)

for i in b:
  print(int(np.round(np.real(i))),end=' ')
print()

""" b = binary(b)
for i in b:
  print(i,end=' ')
print()
N = len(b)

print('FFT:')
b = fft(b)
for i in b:
  print(i,end=' ')
print()

print('Pairwise Multiply:')
b *= b
for i in b:
  print(i,end=' ')
print()

print('Conjugate:')
b = np.conj(b)
for i in b:
  print(i,end=' ')
print()

print('FFT on Conjugate:')
b = fft(b)
for i in b:
  print(i,end=' ')
print()

print('Divide by Double-Length:')
b /= float(2*N)
for i in b:
  print(i,end=' ')
print()

print('Solution Set:')
for i in b:
  print(int(np.round(np.real(i))),end=' ')
print() """

""" b = b[:2*N-1]
for i in b:
  print(i,end=' ')
print() """
