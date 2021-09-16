class view(object):
  def __init__(self, sequence, start):
      self.sequence, self.start = sequence, start
  def __getitem__(self, index):
      return self.sequence[index + self.start]
  def __setitem__(self, index, value):
      self.sequence[index + self.start] = value
def balsub(w, c):
  ''' A balanced algorithm for Subset-sum problem by David Pisinger
  w = weights, c = capacity of the knapsack '''
  n = len(w)
  assert n > 0
  sum_w = 0
  r = 0
  for wj in w:
      assert wj > 0
      sum_w += wj
      assert wj <= c
      r = max(r, wj)
  assert sum_w > c
  b = 0
  w_bar = 0
  while w_bar + w[b] <= c:
      w_bar += w[b]
      b += 1
  s = [[0] * 2 * r for i in range(n - b + 1)]
  s_b_1 = view(s[0], r - 1)
  for mu in range(-r + 1, 1):
      s_b_1[mu] = -1
  for mu in range(1, r + 1):
      s_b_1[mu] = 0
  s_b_1[w_bar - c] = b
  for t in range(b, n):
      s_t_1 = view(s[t - b], r - 1)
      s_t = view(s[t - b + 1], r - 1)
      for mu in range(-r + 1, r + 1):
          s_t[mu] = s_t_1[mu]
      for mu in range(-r + 1, 1):
          mu_prime = mu + w[t]
          s_t[mu_prime] = max(s_t[mu_prime], s_t_1[mu])
      for mu in range(w[t], 0, -1):
          for j in range(s_t[mu] - 1, s_t_1[mu] - 1, -1):
              mu_prime = mu - w[j]
              s_t[mu_prime] = max(s_t[mu_prime], j)
  solved = False
  z = 0
  s_n_1 = view(s[n - b], r - 1)
  while z >= -r + 1:
      if s_n_1[z] >= 0:
          solved = True
          break
      z -= 1
  if solved:
      print(c + z)
      print(n)
      x = [False] * n
      for j in range(0, b):
          x[j] = True
      for t in range(n - 1, b - 1, -1):
          s_t = view(s[t - b + 1], r - 1)
          s_t_1 = view(s[t - b], r - 1)
          while True:
              j = s_t[z]
              assert j >= 0
              z_unprime = z + w[j]
              if z_unprime > r or j >= s_t[z_unprime]:
                  break
              z = z_unprime
              x[j] = False
          z_unprime = z - w[t]
          if z_unprime >= -r + 1 and s_t_1[z_unprime] >= s_t[z]:
              z = z_unprime
              x[t] = True
      for j in range(n):
          print(x[j], w[j])
#balsub([3318,2425,13535,3318,4859,20701,5523,8098,11147,1547,23796,2981,1547,17041,34081,4248,27216,13846,38686,51124,153372,102242,14867,17615,27757,8521,11570,2124,22267,29669,70119,170403,12743,8548,7447,14867,4274,12371,29669,9672,102248,136322,31858,8548,47426,13540,24590,12283,33775,3868,5805,4948,5934,7254,2708,676,3956,2418,4248,677,12371,3956,2418,8521,17041,4274,3070,24566,2264,2290,141298,66930,37184,1484,95861,23938,119826,35948,65905,11983],778592)
balsub([3318,2425,13535,3318,4859,20701],778592011)