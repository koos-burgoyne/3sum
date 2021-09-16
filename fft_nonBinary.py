import numpy
from numpy.fft import fft
from time import time

# this is an r(n) = 2*r(n/2) + \Theta(n) \in \Theta(n log(n)) algorithm:
def _fft(vec):
  n=len(vec)
  if n==1:
    return vec
  result = numpy.array(numpy.zeros(n), numpy.complex128)
  # packed coefficients eliminate zeros. e.g., f(x)=1+2x+3x**2+...,
  # then e(x)=1+3x**2+... = 1+0x+3x**2+0x**3+... = (1+3y+...),y=x**2.
  packed_evens = vec[::2]
  packed_odds = vec[1::2]
  # packed_evens(x**2) and packed_odds(x**2) for the first half of x
  # points. The other half of the points are the negatives of the
  # first half (used below).
  fft_evens = fft(packed_evens)
  fft_odds = fft(packed_odds)
  
  # Butterfly:
  for i in range(int(n/2)):
    # result = evens(x) + x*odds(x), where x is a complex root of unity
    #        = packed_evens(x**2) + x*packed_odds(x**2)
    x = numpy.exp(-2*numpy.pi*i*1j/n)
    j = x * fft_odds[i]
    result[i] = fft_evens[i] + j
    result[i + int(n/2)] = fft_evens[i] - j
  return result

if __name__=='__main__':
  #N=2**3
  #x=numpy.array(numpy.arange(N),float)
  x = [5,3,2,1]
  
  print()
  t1=time()
  recursive_result = _fft(x)
  t2=time()
  print('Recursive FFT took', t2-t1, 'seconds\n')

  print(recursive_result)

  print()
  t1=time()
  numpy_result = fft(x)
  t2=time()
  print('Numpy FFT took', t2-t1, 'seconds\n')
