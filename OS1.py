
def OrderedSet(alist):
  """ Creates an ordered set from a list of tuples or other hashable items """
  mmap = {} # implements hashed lookup
  oset = [] # storage for set
  for item in alist:
    #Save unique items in input order 
    if item not in mmap:
      mmap[item] = 1
      oset.append(item)
  return oset