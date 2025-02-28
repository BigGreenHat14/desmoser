import desmoser
import math
obj = match_case(var("op"),[
    a + b,a - b,a * b,a / b,a ** b,a % b,a // b,a.nth_root()
])
print(obj.convert_to_expression(var("calc"),var("res")))