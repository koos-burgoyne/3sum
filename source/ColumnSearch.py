import numpy as np

# column search
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