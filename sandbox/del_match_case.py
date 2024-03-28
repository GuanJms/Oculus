def match_case(x, y):
    match x:
        case 2 if y == 1:
            print("1 == 1")
        case 3 if y == 2:
            print("1 == 2")

match_case(x=3, y =2)