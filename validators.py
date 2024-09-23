def sum(items):
  sum = 0
  for i in items:
    sum += i
  return sum

def is_balanced_case(source, destination):
  return sum(source) == sum(destination)