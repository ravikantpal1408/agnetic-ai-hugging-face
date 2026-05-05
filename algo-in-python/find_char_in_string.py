def find_char_in_str(input_str: str):
    frequency = {}
    for char in input_str:
        frequency[char] = frequency.get(char, 0) + 1

    return frequency


input_str = input("Please enter any text : \n")

print(find_char_in_str(input_str))
