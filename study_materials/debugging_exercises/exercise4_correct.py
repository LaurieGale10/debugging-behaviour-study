#This program should display the first 12 multiples of the number 6 using a while loop, from 1x6 up to 12x6. Fix the errors to make sure it prints them properly.
#This program has 4 errors

count="1"
print("The first 12 multiples of the number 6 are:")
while count<12:
    times_table = 6 * count
    count=count+1
print(times_Table)


#Errors:
# TypeError with variable i; should be an integer rather than a string
# i<12 on line 6 should be i<=12
# The print statement on line 9 should be printed so the value is printed after each iteration of the while loop
# NameError on line 9 due to typo in variable name "times_table"