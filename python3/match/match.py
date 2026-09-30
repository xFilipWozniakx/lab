day = 4
match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case 4:
        print("Thursday")
    case 5:
        print("Friday")
    case 6:
        print("Saturday")
    case 7:
        print("Sunday")
    case _:
        print("wrong number day specified")

# or combined values in match expression:
match day:
    case 1 | 2 | 3 | 4 | 5:
        print("week day")
    case 6 | 7:
        print("weekend")

# or combined match statements with if statements:
month = "March"
day = 5
match day:
    case 1 | 2 | 3 | 4 | 5 if month == "April":
        print("week day in April")
    case 6 | 7 if month == "April":
        print("weekend in april")
    case 1 | 2 | 3 | 4 | 5 if month == "March":
        print("week day in March")
    case 6 | 7 if month == "March":
        print("weekend in March")
