import random

lower_bond = int(input("Enter the lower bond: "))
upper_bond = int(input("Enter the upper bond: "))
def generate_random_number(lower, upper):
    return random.randint(lower,upper)

result = generate_random_number(lower_bond, upper_bond)
print(result)