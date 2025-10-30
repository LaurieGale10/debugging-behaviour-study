print("This program will check if you should apply to be a computing teacher")
age = int(input("What is your age? "))
computing_degree = input("Do you have a passion for teaching computing? Enter 'yes' or 'no': ")

if age >= 21 and computing_degree == "Yes":
    allowed_to_apply = "Successful"
else:
    allowed_to_apply = "Unsuccessful"
print("Result of check:",allowed_to_apply)