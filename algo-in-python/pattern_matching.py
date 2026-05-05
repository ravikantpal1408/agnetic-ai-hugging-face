def find_vowels_and_constants_str(input_str: str):
    vowels = "aeiouAEIOU"
    constant_list = []
    vowels_list = []

    for char in input_str:
        if char.isalpha():
            if char in vowels:
                vowels_list.append(char)
            else:
                constant_list.append(char)

    return vowels_list, constant_list


input_str = input("Please input any string \n")

v, c = find_vowels_and_constants_str(input_str)
print(f"vowels {v} \n")
print(f"constant {c}")
