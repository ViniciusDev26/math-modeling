def read_txt_file(filename):
  f = open(filename, "r")
  content = []
  while True:
    line = f.readline()
    if not line:
      break
    formatted_line = line.replace("\n", "").split(" ")
    num_arr = list(map(int, formatted_line))

    content.append(num_arr)
  return content
