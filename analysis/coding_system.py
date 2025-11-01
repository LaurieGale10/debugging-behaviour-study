import csv
from analysis.core_filter_functions import *
from analysis.stats_functions import *

def save_code_counts():
    """Records and saves the count of each code (in terms of program logs and number of students who demonstrate the code) to a csv
    """
    #A list of all the codes in the new coding system, comprised of "non-codeable sub-categories" and "codeable" codes whose names have been refactored based on what they are in the PDA tool
    #Would be good to maintain this list (as well as a list that contains the actual names of each code as they appear in the paper. Ultimately this whole system needs clearing up a little bit
    codes = ["First move",
    "Made changes before running code",
    "Ran code before making changes",
    "Introduced additional error(s)",
    "Reverted corrective change(s)",
    "Introduced additional syntax error(s)",
    "Incorrect syntactical changes to existing statements",
    "Incorrect syntactical changes to output statements",
    "Incorrect syntactical changes involving selection",
    "Incorrect syntactical changes involving iteration",
    "Incorrect syntactical changes to variable assignments",
    "Incorrect syntactical changes involving other statements in program",
    "Incorrect syntactical changes involving symbols",
    "Incorrect syntactical changes to operators",
    "Incorrect syntactical changes to mathematical operators",
    "Incorrect syntactical changes to logical operators",
    "Incorrect syntactical changes to other symbols",
    "Incorrect syntactical changes involving fusion or distribution of multiple lines of code",
    "Addition of non-language-specific strings",
    "Incorrect syntactical changes involving variable references",
    "Incorrect syntactical changes to whitespace of program",
    "Introduced additional runtime error(s)",
    "Incorrect semantic changes to variable assignments",
    "Incorrect semantic changes to variable references",
    "Incorrect semantic changes to other statements in program",
    "Introduced additional type error(s)",
    "Incorrect typewise changes involving variables",
    "Incorrect typewise changes to function call",
    "Incorrect typewise changes to other statements in program",
    "Introduced additional logical error(s)",
    "Logically incorrect changes involving output statements",
    "Logically incorrect changes to operators",
    "Logically incorrect changes to mathematical operators",
    "Logically incorrect changes to logical operators",
    "Logically incorrect changes involving variables",
    "Logically incorrect changes to program flow",
    "Logically incorrect changes to other statements",
    "Resolved error(s)",
    "Resolved syntax error(s)",
    "Correctly resolved syntax error",
    "Resolved syntax error by changing syntax of erroneous component",
    "Introduced logical error from resolution of syntax error",
    "Hard-coded resolution of syntax error",
    "Resolved runtime error(s)",
    "Correctly resolved runtime error",
    "Introduced logical error from resolution of runtime error",
    "Hard-coded resolution of runtime error",
    "Resolved type error(s)",
    "Correctly resolved type error",
    "Hard-coded resolution of type error",
    "Resolved logical error(s)",
    "Correctly resolved logical error",
    "Correctly resolved logical error while code not running",
    "Correctly resolved logical error after a single successful run",
    "Correctly resolved logical error after repeated successful runs",
    "Hard-coded resolution of logical error",
    "Positive debugging indicators",
    "Entered incorrect input (implies testing)",
    "Made improvements to program",
    "First change on line referred to in error message",
    "Inconsequential changes",
    "Addition/removal or editing of comments",
    "Inconsequential changes involving symbols",
    "Inconsequential changes to variable references",
    "Inconsequential changes to whitespace of program",
    "Changes to existing statements in the program",
    "Inconsequential changes to (existing) outputs",
    "Inconsequential changes to (existing) inputs",
    "Inconsequential changes to (existing) other statements",
    "Addition of unnecessary code",
    "Miscellaneous behaviour",
    "Repeated runs",
    "Repeated successful runs when code successfully runs",
    "Repeated unsuccessful runs with no changes",
    "Repeatedly ran code with no changes at beginning of exercise",
    "Reverted previous changes",
    "Didn't attempt exercise"]

    with open("code_counts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for code in codes:
            n_participants_with_code = length_of_participants_list(filtered_ids=filter_participants_with_codes([code]))
            n_program_logs_with_code = length_of_program_logs_list(filtered_ids=filter_program_logs_with_codes([code]))
            if n_participants_with_code == None and n_participants_with_code == None:
                writer.writerow([code])
            else:
                writer.writerow([code, n_participants_with_code, round((n_participants_with_code / 73) * 100, 2), n_program_logs_with_code, round((n_program_logs_with_code / 322) * 100, 2)])

save_code_counts()