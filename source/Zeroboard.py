
# zeroboard approach
def solve(x):
  n = len(x)-1
  
  # get first column to include in zeroBoard: time < N
  start_col = 0
  while (x[start_col]+x[start_col]+x[n]) < 0:
    start_col += 1

  # get last column to include in zeroBoard: time < N
  end_col = start_col
  while (x[0]+x[end_col]+x[end_col]) < 0 and end_col < (n):
    end_col += 1
  if end_col != n: end_col -= 1

  zeroboard_size = end_col-start_col+1

  # create key sequence to get zeroBoard column heights: time < N
  key_seq = {}
  prev = 0
  for i in range(n-1,-1,-1):
    key_seq[-(prev + x[i] - x[i+1])] = i + 1
    prev += (x[i] - x[i+1])  
  
  # store edge margins: time < N
  top_edges = [0]*(zeroboard_size)
  bottom_edges = [0]*zeroboard_size
  for i in range(start_col,end_col+1):
    if i == start_col: top = 0
    else:
      top = top_edges[i-start_col-1]
      while (x[start_col]+x[i]+x[n-top]) >= 0 and n-top > i:
        top += 1
    top_edges[i-start_col] = top

    if i == start_col: bottom = 0
    else:
      bottom = bottom_edges[i-start_col-1]
      while x[0]+x[i]+x[n-bottom] < 0 and bottom > 0:
        bottom -= 1
    bottom_edges[i-start_col] = bottom

  # add columns to zeroboard: time UNKNOWN
  zbSize = 0
  zeroboard_tip = x[0]+x[n]+x[n]
  zeroboard_1 = [0] * int(x[n]-x[0]*2)
  zeroboard_2 = [0] * int(x[n]-x[0]*2)
  for i in range(0, zeroboard_size):
    start = i + start_col
    for j in range(0, top_edges[i]-bottom_edges[i]+1):
      zbSize += 1
      insertion_value = zeroboard_tip - (x[0]+x[start]+x[n-(j+bottom_edges[i])])
      if zeroboard_1[insertion_value] == 0:
        zeroboard_1[insertion_value] = []
        zeroboard_2[insertion_value] = []
        zeroboard_1[insertion_value].append(x[start])
        zeroboard_2[insertion_value].append(x[n-(j+bottom_edges[i])])
      else:
        zeroboard_1[insertion_value].append(x[start])
        zeroboard_2[insertion_value].append(x[n-(j+bottom_edges[i])])

  final_pair = x[n]+x[n]
  first_check_val = 0
  while (x[first_check_val]+final_pair) < 0:
    first_check_val += 1
  last_check_val = start_col
  while (x[last_check_val]+x[last_check_val]+x[last_check_val]) < 0:
    last_check_val += 1
  
  # check zeroboard for zeros: time < N*(width of zeroBoard at a maximum) -> find the max possible width of a zeroboard in relation to N and we have a runtime
  solutions = []
  for i in range(first_check_val,last_check_val):
    val_to_check = x[i] + final_pair
    if zeroboard_1[val_to_check] != 0:
      solutions.append([x[i],zeroboard_1[val_to_check],zeroboard_2[val_to_check]])

  return solutions