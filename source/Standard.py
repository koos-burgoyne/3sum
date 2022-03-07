# Synopsis: The globally accepted standard implementation for the 3sum algorithm 
# Args    : An list of integers
# Runtime : O(n**2)
# Returns : List of triplets summing to zero
def threeSum(nums):
  n=len(nums)
  result = []
  for i in range(0,n-2):
    a = nums[i]
    start = i+1
    end = n-1
    while (start<end):
      b = nums[start]
      c= nums[end]
      if (a+b+c) == 0:
        result.append([a,b,c])
        start += 1
        end -= 1
      elif (a+b+c) > 0:
        end -= 1
      else:
        start += 1
  return result