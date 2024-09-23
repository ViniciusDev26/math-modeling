from read_txt_file import read_txt_file
from validators import is_balanced_case

file_path = "./data/case-1.txt"
content = read_txt_file(file_path)

[quantity_source, quantity_destination] = content[0]
quantity_source_per_source = content[1]
quantity_destination_per_destination = content[2]
is_balanced = is_balanced_case(quantity_source_per_source, quantity_destination_per_destination)

for i in range(3, len(content)):
  print(content[i])

