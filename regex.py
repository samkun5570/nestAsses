import re
# import json

result = {"orders":[{"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6},{"id":7},{"id":8},{"id":9},{"id":10},{"id":11},{"id":648},{"id":649},{"id":650},{"id":651},{"id":652},{"id":653}],"errors":[{"code":3,"message":"[PHP Warning #2] count(): Parameter must be an array or an object that implements Countable (153)"}]}

#using list comprehension
id_and_code_list_com= [orders["id"] for orders in result["orders"]] + [errors["code"] for errors in result["errors"]]
print('Numbers generated from json using list comprehention',id_and_code_list_com)

#using regex
# result_string = json.dumps(result)
result_string = str(result)
print('Numbers generated from json using re  after converting to string', [int(num.split(' ')[1]) for num in re.findall(r': \d+', result_string)] )

#using regex with lamda and map
numb_regex =list(map(lambda x: int(x.split(' ')[1]),re.findall(r': \d+', result_string)))
print('Numbers generated from json using re  after converting to string', numb_regex )
