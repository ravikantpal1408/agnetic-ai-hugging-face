def check_for_pallindrom(inputstr: str):
    p2 = len(inputstr) - 1
    p1 = 0
    check = True
    while p1 <= p2:
        if inputstr[p1] == inputstr[p2]:
            p1 = p1 + 1
            p2 = p2 - 1
        else:
            check = False
            break

    if check:
        print("String is pallindrome")
    else:
        print("String is not Pallindrome")


str_input = input("Enter a string to check pallindrome : \n")

check_for_pallindrom(str_input)
