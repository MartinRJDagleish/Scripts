

def stdout_to_numpy(input_str: str) -> list[list[float]]:
    input_str = input_str.strip().split("\n") 
    matr = [[float(num) for num in line.split()] for line in input_str]
    return matr
