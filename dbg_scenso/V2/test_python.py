#/bin/env python3
#
# input_num = 8
# max_product = 0
# num1 = 0
# num2 = 0
#
# for i in range(1, input_num // 2 + 1):
#     j = input_num - i
#     product = i * j
#     if product > max_product:
#         max_product = product
#         num1 = i
#         num2 = j
#
# print(f"Input: {input_num}")
# print(f"Largest product: {max_product}")
# print(f"Numbers: ({num1}, {num2})")

def find_largest_product(input_num):
    max_product = 0
    num1 = 0
    num2 = 0

    for i in range(1, input_num // 2 + 1):
        j = input_num // i
        if i * j == input_num and j >= i:
            product = i * j
            if product > max_product:
                max_product = product
                num1 = i
                num2 = j

    return (num1, num2)

# Example usage
input_num = 8
result = find_largest_product(input_num)
print(f"Input: {input_num}")
print(f"Largest product: {input_num}")
print(f"Numbers: {result}")
