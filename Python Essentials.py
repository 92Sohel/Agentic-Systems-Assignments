try:
    num1 = int(input("please type a number"))
    num2 = int(input("please type a number"))
    print("The sum of two numbers is", num1+num2)

    if num2==0:
        print("can't devide by zero")
    else:
        print("Division result:-", num1/num2)

except ValueError:
    print("invalid input")



