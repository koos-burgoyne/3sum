import numpy
from scipy.signal import fftconvolve

class PMF:
  def __init__(self, start_value, masses):
    self._start_value = start_value
    self._masses = numpy.array(masses, float)
    self._masses /= sum(self._masses)
  
  def size(self):
    return len(self._masses)
  
  def narrowed_to_intersecting_support(self, rhs):
    start_value = max(self._start_value, rhs._start_value)
    end_value = min(self._start_value+self.size() - 1,
    rhs._start_value+rhs.size() - 1)
    masses = self._masses[start_value - self._start_value:]
    end_size = end_value - start_value + 1
    masses = masses[:end_size]
    return PMF(start_value, masses)
  
  def __add__(self, rhs):
    return PMF(self._start_value + rhs._start_value,fftconvolve(self._masses, rhs._masses))
  
  def __sub__(self, rhs):
    return PMF(self._start_value - (rhs._start_value+rhs.size()-1),fftconvolve(self._masses, rhs._masses[::-1]))
  def __mul__(self, rhs):
    this = self.narrowed_to_intersecting_support(rhs)
    rhs = rhs.narrowed_to_intersecting_support(self)
    # now the supports are aligned:
    return PMF(this._start_value, this._masses*rhs._masses)
  def support(self):
    return list(xrange(self._start_value, self._start_value+self.size()))
  def support_contains(self, outcome):
    return outcome >= self._start_value and outcome < self._start_value + self.size()
  def get_probability(self, outcome):
    return self._masses[outcome - self._start_value]
  def __str__(self):
    result = 'PMF('
    for i in xrange(self.size()):
      mass = self._masses[i]
      result += str(self._start_value + i) + ':' + str(numpy.round(mass,4))
    if i != self.size()-1:
      result += '\t'
    result += ')'
    return result
  def __repr__(self):
    return str(self)
import itertools
# runtime is \in \Omega(k^n)
def brute_force_solve(prior_pmfs, likelihood_pmf):
  # prior_pmfs = [X_0, X_1, ...]
  # likelihood_pmf = Y|D
  # compute prior of Y:
  prior_supports = [ pmf.support() for pmf in prior_pmfs ]
  all_joint_events = itertools.product(*prior_supports)
  
  prior_of_y = [0.0]*likelihood_pmf.size()
  for joint_event in all_joint_events:
    y = sum(joint_event)
    if likelihood_pmf.support_contains(y):
      probability = numpy.product([ pmf.get_probability(event) for event,pmf in zip(joint_event,prior_pmfs) ])
      prior_of_y[y-likelihood_pmf._start_value] += probability
  prior_of_y = PMF(likelihood_pmf._start_value, prior_of_y)
  
  # compute likelihoods X_1|D, X_2|D, ...
  likelihoods = []
  for i in xrange(len(prior_pmfs)):
    priors_without_i = [ prior_pmfs[j] for j in xrange(len(prior_pmfs))
    if j != i ]
    distributions = priors_without_i + [likelihood_pmf]
    
    supports = [ pmf.support() for pmf in priors_without_i ] + [likelihood_pmf.support() ]
    all_joint_events = itertools.product(*supports)
    
    result_i = [0.0]*prior_pmfs[i].size()
    for joint_event in all_joint_events:
      y = joint_event[-1]
      sum_x_without_i = sum(joint_event[:-1])
      probability = numpy.product([ pmf.get_probability(event) for event,pmf in zip(joint_event,distributions) ])
      
      x_i = y - sum_x_without_i
      if prior_pmfs[i].support_contains(x_i):
        result_i[x_i - prior_pmfs[i]._start_value] += probability
      result_i = PMF(prior_pmfs[i]._start_value, result_i)
      result_i = result_i.narrowed_to_intersecting_support(prior_pmfs[i])
      likelihoods.append(result_i)

  return likelihoods, prior_of_y

# runtime is \in \Theta(n k \log(n k) \log(n))
def convolution_tree_solve(prior_pmfs, likelihood_pmf):
  # prior_pmfs = [X_0, X_1, ...]
  # likelihood_pmf = Y|D
  n = len(prior_pmfs)
  
  # forward pass:
  layer_to_priors = []
  layer_to_priors.append(prior_pmfs)
  
  while len(layer_to_priors[-1]) > 1:
    layer = []
    for i in xrange(len(layer_to_priors[-1])/2):
      layer.append( layer_to_priors[-1][2*i] + layer_to_priors[-1][2*i+1])
    if len(layer_to_priors[-1]) % 2 != 0:
      layer.append(layer_to_priors[-1][-1])
    layer_to_priors.append(layer)
  
  layer_to_priors[-1][0] = layer_to_priors[-1][0].narrowed_to_intersecting_support(likelihood_pmf)
  
  # backward pass:
  layer_to_likelihoods = [ [likelihood_pmf] ]
  
  for i in xrange(1, len(layer_to_priors)):
    # j is in {1, ... len(layer_to_priors) - 1}
    j = len(layer_to_priors) - i
    layer = []
    for k in xrange(len(layer_to_priors[j])):
      parent_likelihood = layer_to_likelihoods[-1][k]
      if 2*k+1 < len(layer_to_priors[j-1]):
        # this PMF came from two parents during merge step:
        lhs_prior = layer_to_priors[j-1][2*k]
        rhs_prior = layer_to_priors[j-1][2*k+1]
        lhs_likelihood = parent_likelihood - rhs_prior
        rhs_likelihood = parent_likelihood - lhs_prior
        lhs_likelihood = lhs_likelihood.narrowed_to_intersecting_support(lhs_prior)
        rhs_likelihood = rhs_likelihood.narrowed_to_intersecting_support(rhs_prior)
        layer.append(lhs_likelihood)
        layer.append(rhs_likelihood)
      else:
        # this PMF came from one parent during merge step (because
        # previous layer was not divisible by 2):
        layer.append(layer_to_priors[j-1][2*k])
    # todo: adapt where not multiple of 2
    layer_to_likelihoods.append(layer)
  layer_to_likelihoods = layer_to_likelihoods[::-1]
  
  # returns likelihoods X_0|D, X_1|D, ... and prior for Y
  return (layer_to_likelihoods[0], layer_to_priors[-1][0])

A = PMF(3, [0.5,0,0.5])
print ('A', A)
print
B = PMF(1, [1,0,0])
print ('B', B)
print
C = PMF(0, [0,0.5,0.5])
print ('C', C)
print
D = PMF(4, [0,0.333,0.0,0.0,0.333,0.333])
print ('D', D)
print

print ('convolution tree:')
likelihoods, prior = convolution_tree_solve([A,B,C], D)
print ('prior D', prior)
print ('likelihoods A,B,C', likelihoods)