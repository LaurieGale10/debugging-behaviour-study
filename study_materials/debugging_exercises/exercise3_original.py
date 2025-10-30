# Initial description
#This program checks if someone should apply to be a computing teacher using the steps below:
# Input the user's age
# Input the user's response to the question "Do you have a passion for teaching computing? Enter 'yes' or 'no': "
# If the user is 21 or over and does have a passion for teaching computing, the check should be a success.
# Otherwise, the check should be unsuccessful.
#This program has 4 errors.

print("This program will check if you should apply to be a computing teacher")
age = int(input("What is your age? "))
computing_degree = input("Do you have a passion for teaching computing? Enter 'yes' or 'no': ")

if age >= 21 and computing_degree = "Yes":
    allowed_to_apply = "Successful"
else:
    allowed_to_apply = "Unsuccessful"
    print("Result of check:",allowed_to_apply)

#Errors:
# age>21 should be age>=21
# Should be a double equals on line 13 when checking the value of the string
# The or on line 13 should be an and
# Line 17 should not be indented so that the result of the check will always be printed
