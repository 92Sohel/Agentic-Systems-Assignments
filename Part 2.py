try : 

    first_name = input("please enter your first name?")
    last_name = input("please enter your last name?")
    age = int(input("please enter your age"))

    print("full name :",first_name+" "+last_name)

    if age<=0:
        print("Age cant be negative")
    else:
        print(f"you'll be {age+1} years old next year")

except ValueError :
    print("Invalid age Input")


