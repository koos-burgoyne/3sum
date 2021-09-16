import numpy
from time import time
# this is an r(n) = 2*r(n/2) + \Theta(n) \in \Theta(n log(n)) algorithm:
def fft(vec):
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
  for i in xrange(n/2):
    # result = evens(x) + x*odds(x), where x is a complex root of unity
    #        = packed_evens(x**2) + x*packed_odds(x**2)
    x = numpy.exp(-2*numpy.pi*i*1j/n)
    result[i] = fft_evens[i] + x * fft_odds[i]
  for i in xrange(n/2,n):
    # result = evens(x) + x*odds(x), where x is a complex root of unity
    #        = packed_evens(x**2) + x*packed_odds(x**2)
    x=numpy.exp(-2*numpy.pi*i*1j/n)
    # first half of points are negative of second half.
    # x_i = -x_{i+n/2}, x_i**2 = x_{i+n/2}**2; therefore
    # packed_evens(x_i**2) = packed_evens(x_{i+n/2}**2) and
    # packed_odds(x_i**2) = packed_odds(x_{i+n/2}**2)
    result[i] = fft_evens[i - n/2] + x * fft_odds[i - n/2]
  return result

if __name__=='__main__':
  #N=2**3
  #x=numpy.array(numpy.arange(N),float)
  x = [0,1,2,3]
  y = [3,2,1,1]
  print (x, y)
  t1=time()
  numpy_result_x = numpy.fft.fft(x)
  numpy_result_y = numpy.fft.fft(y)
  addition_result = [0] * len(x)
  for item in range(0,4):
    addition_result[item] = numpy_result_x[item] + numpy_result_y[item]
  final = numpy.fft.ifft(addition_result)
  print ('answer: ', final)
  t2=time()
  #print 'numpy fft:', numpy_result_x, numpy_result_y
  print ('took', t2-t1, 'seconds')


  """
  print
  t1=time()
  recursive_result = fft(x)
  t2=time()
  print 'fast ft:', recursive_result
  print 'took', t2-t1, 'seconds'
  print
  print 'Largest error', max(numpy.abs(numpy_result - recursive_result))
  print 'Recursive python FFT took', t2-t1, 'seconds'
  """