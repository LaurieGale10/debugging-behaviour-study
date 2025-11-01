import os
import psycopg2
from analysis.core_filter_functions import *

"""Filter participants based on survey responses"""

#TODO: Change these to be more scalable - shouldn't be referencing database here. Can't it be done using the participants table in kwargs?

def filter_female_students(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantIds for participants who reported their gender as female"""
    connection = psycopg2.connect( #TODO: Make connection pool
            host = os.environ['DB_HOST_IP'],
            port = os.environ['DB_PORT'],
            database = 'program_data',
            user = os.environ['DB_USERNAME'],
            password = os.environ['DB_PASSWORD']
        )
    cursor = connection.cursor()
    cursor.execute("SELECT participantid FROM participants WHERE gender = 'Female';")
    data = DataFrame(cursor.fetchall())
    if data.empty:
        return {}
    filtered_id_dict = {}
    data.columns = [description[0] for description in cursor.description]
    female_participant_ids = data["participantid"].values.tolist()
    filtered_id_dict["participantids"] = female_participant_ids
    cursor.close()
    connection.close()
    return filtered_id_dict

def filter_male_students(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantIds for participants who reported their gender as male"""
    connection = psycopg2.connect( #TODO: Make connection pool
            host = os.environ['DB_HOST_IP'],
            port = os.environ['DB_PORT'],
            database = 'program_data',
            user = os.environ['DB_USERNAME'],
            password = os.environ['DB_PASSWORD']
        )
    cursor = connection.cursor()
    cursor.execute("SELECT participantid FROM participants WHERE gender = 'Male';")
    data = DataFrame(cursor.fetchall())
    if data.empty:
        return {}
    filtered_id_dict = {}
    data.columns = [description[0] for description in cursor.description]
    male_participant_ids = data["participantid"].values.tolist()
    filtered_id_dict["participantids"] = male_participant_ids
    cursor.close()
    connection.close()
    return filtered_id_dict

"""Filter based on end state of debugging exercises"""

def filter_by_students_who_ended_all_attempted_exercises_in_correct_state(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantids for participants who ended each attempted exercise in a correct state.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who ended each attempted exercise in a correct state.
    """
    return filter_participants_with_codes(["Ended exercise in correct state"], ["Ended exercise with logical error(s)", "Ended exercise with runtime error(s)", "Ended exercise with syntax error(s)", "Ended exercise with type error(s)"])

def filter_by_students_who_ended_all_attempted_exercises_in_incorrect_state(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantids for participants who ended each attempted exercise in an incorrect state.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who ended each attempted exercise in an incorrect state.
    """
    return filter_participants_with_codes(["Ended exercise with logical error(s)", "Ended exercise with runtime error(s)", "Ended exercise with syntax error(s)", "Ended exercise with type error(s)"], ["Ended exercise in correct state"])

#For these functions, we need to get the count of the error code, which must be equal to the number of attempted exercises
#Might be easier to do with DataFrames rather than write a separate query?

def filter_all_students_who_ended_all_attempted_exercises_with_syntax_errors(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantids for participants who ended each attempted exercise with syntax errors.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who ended each attempted exercise with syntax errors.
    """
    raise NotImplementedError("Filter has not been implemented yet")

def filter_all_students_who_ended_all_attempted_exercises_with_runtime_errors(**kwargs) -> dict[str, list[str]]:
    """Filters all students who ended all attempted exercises with runtime errors.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who ended each attempted exercise with runtime errors.
    """
    raise NotImplementedError("Filter has not been implemented yet")

def filter_all_students_who_ended_all_attempted_exercises_with_type_errors(**kwargs) -> dict[str, list[str]]:
    """Filters all students who ended all attempted exercises with type errors.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who ended each attempted exercise with type errors.
    """
    raise NotImplementedError("Filter has not been implemented yet")

def filter_all_students_who_ended_all_attempted_exercises_with_logical_errors(**kwargs) -> dict[str, list[str]]:
    """Filters all students who ended all attempted exercises with logical errors.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who ended each attempted exercise with logical errors.
    """
    raise NotImplementedError("Filter has not been implemented yet")

def filter_program_logs_in_correct_end_state(**kwargs) -> dict[str, list[str]]:
    """Gets the list of programlogids for logs that end in the correct state.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of programlogids (under the key 'programlogids') that ended in a correct state.
    """
    return filter_program_logs_with_codes(["Ended exercise in correct state"], ["Ended exercise with logical error(s)", "Ended exercise with runtime error(s)", "Ended exercise with syntax error(s)", "Ended exercise with type error(s)"])

def filter_program_logs_ending_with_errors(**kwargs) -> dict[str, list[str]]: #TODO: Not working properly, same for filter_by_students_who_ended_all_attempted_exercises_in_incorrect_state?
    """Gets the list of programlogids for logs that end with errors.
    
    Returns:
        dict[str, list[str]]: A dictionary containing a list of programlogids (under the key 'programlogids') that ended with errors.
    """    
    return filter_participants_with_codes(["Ended exercise with logical error(s)", "Ended exercise with runtime error(s)", "Ended exercise with syntax error(s)", "Ended exercise with type error(s)"], ["Ended exercise in correct state"])

def filter_unattempted_program_logs(**kwargs) -> dict[str, list[str]]:
    """Gets all the program logs that were not attempted, according to the code "Didn't attempt exercise".
    
    Returns:
        dict[str, list[str]]: A dictionary containing a list of programlogids (under the key 'programlogids') that were not attempted.
    """
    return filter_program_logs_with_codes(["Didn't attempt exercise"])

"""Filter by students introduced and resolved errors"""

def filter_students_who_introduced_syntax_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who introduced an additional syntax error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal syntax error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who introduced a syntax error.
    """
    introduced_syntax_error_codes = ["Addition of non-language-specific strings",
                                    "Incorrect syntactical changes involving fusion or distribution of multiple lines of code",
                                    "Incorrect syntactical changes involving iteration",
                                    "Incorrect syntactical changes involving other statements in program",
                                    "Incorrect syntactical changes involving selection",
                                    "Incorrect syntactical changes involving variable references",
                                    "Incorrect syntactical changes to logical operators",
                                    "Incorrect syntactical changes to mathematical operators",
                                    "Incorrect syntactical changes to other symbols",
                                    "Incorrect syntactical changes to output statements",
                                    "Incorrect syntactical changes to variable assignments",
                                    "Incorrect syntactical changes to whitespace of program"]
    return filter_participants_with_codes(introduced_syntax_error_codes)

def filter_students_who_introduced_runtime_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who introduced an additional runtime error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal runtime error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who introduced a runtime error.
    """
    introduced_runtime_error_codes = ["Incorrect semantic changes to other statements in program",
                                    "Incorrect semantic changes to variable assignments",
                                    "Incorrect semantic changes to variable references"]
    return filter_participants_with_codes(introduced_runtime_error_codes)

def filter_students_who_introduced_type_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who introduced an additional type error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal type error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who introduced a type error.
    """
    introduced_type_error_codes = [ "Incorrect typewise changes involving variables",
                                    "Incorrect typewise changes to function call",
                                    "Incorrect typewise changes to other statements in program"]
    return filter_participants_with_codes(introduced_type_error_codes)

def filter_students_who_introduced_logical_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who introduced an additional logical error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal logical error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who introduced a logical error.
    """
    introduced_logical_error_codes = ["Logically incorrect changes involving output statements",
                                    "Logically incorrect changes involving variables",
                                    "Logically incorrect changes to logical operators",
                                    "Logically incorrect changes to mathematical operators",
                                    "Logically incorrect changes to other statements",
                                    "Logically incorrect changes to program flow",
                                    "Introduced logical error from resolution of runtime error",
                                    "Introduced logical error from resolution of syntax error"]
    return filter_participants_with_codes(introduced_logical_error_codes)

def filter_students_who_introduced_logical_error_through_resolution(**kwargs) -> dict[str, list[str]]:
    """Filters students who resolved at least one error by introducing a logical error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal logical error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who resolved an error by introducing a logical error.
    """
    introduced_logical_error_codes = ["Introduced logical error from resolution of runtime error",
                                    "Introduced logical error from resolution of syntax error"]
    return filter_participants_with_codes(introduced_logical_error_codes)

def filter_students_who_introduced_any_error(**kwargs) -> dict[str, list[str]]:
    """Filters students who introduced at least one error in at least one of their attempted exercises, using a list of codes associated with introducing errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who introduced an error.
    """
    introduced_error_codes = ["Addition of non-language-specific strings",
                              "Incorrect syntactical changes involving fusion or distribution of multiple lines of code",
                              "Incorrect syntactical changes involving other statements in program",
                              "Incorrect syntactical changes involving selection",
                              "Incorrect syntactical changes involving variable references",
                              "Incorrect syntactical changes to logical operators",
                              "Incorrect syntactical changes to mathematical operators",
                              "Incorrect syntactical changes to other symbols",
                              "Incorrect syntactical changes to output statements",
                              "Incorrect syntactical changes to variable assignments",
                              "Incorrect syntactical changes to whitespace of program",
                              "Incorrect semantic changes to other statements in program",
                              "Incorrect semantic changes to variable assignments",
                              "Incorrect semantic changes to variable references",
                              "Incorrect typewise changes involving variables",
                              "Incorrect typewise changes to function call",
                              "Incorrect typewise changes to other statements in program",
                              "Logically incorrect changes involving output statements",
                              "Logically incorrect changes involving variables",
                              "Logically incorrect changes to logical operators",
                              "Logically incorrect changes to mathematical operators",
                              "Logically incorrect changes to other statements",
                              "Logically incorrect changes to program flow",
                              "Introduced logical error from resolution of runtime error",
                              "Introduced logical error from resolution of syntax error"]
    return filter_participants_with_codes(introduced_error_codes)

def filter_students_who_resolved_syntax_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who resolved at least one syntax error in at least one of their attempted exercises, using a list of codes associated with resolving syntax errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who resolved a syntax error.
    """
    resolved_syntax_error_codes = ["Correctly resolved syntax error",
                                   "Hard-coded resolution of syntax error",
                                   "Introduced logical error from resolution of syntax error",
                                   "Resolved syntax error by changing syntax of erroneous component"]
    return filter_participants_with_codes(resolved_syntax_error_codes)

def filter_students_who_resolved_runtime_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who resolved at least one runtime error in at least one of their attempted exercises, using a list of codes associated with resolving runtime errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who resolved a runtime error.
    """
    resolved_runtime_error_codes = ["Correctly resolved runtime error",
                                    "Hard-coded resolution of runtime error",
                                    "Introduced logical error from resolution of runtime error"]
    return filter_participants_with_codes(resolved_runtime_error_codes)

def filter_students_who_resolved_type_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who resolved at least one type error in at least one of their attempted exercises, using a list of codes associated with resolving type errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who resolved a type error.
    """
    resolved_type_error_codes = ["Correctly resolved type error",
                                 "Hard-coded resolution of type error"]
    return filter_participants_with_codes(resolved_type_error_codes)

def filter_students_who_resolved_logical_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who resolved at least one logical error in at least one of their attempted exercises, using a list of codes associated with resolving logical errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who resolved a logical error.
    """
    resolved_logical_error_codes = ["Correctly resolved logical error after a single successful run",
                                    "Correctly resolved logical error after repeated successful runs", 
                                    "Correctly resolved logical error while code not running",
                                    "Hard-coded resolution of logical error"]
    return filter_participants_with_codes(resolved_logical_error_codes)

def filter_students_who_resolved_any_error(**kwargs) -> dict[str, list[str]]:
    """Filters students who resolved at least one error in at least one of their attempted exercises, using a list of codes associated with resolving errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who resolved an error.
    """
    resolved_error_codes = ["Correctly resolved syntax error",
                            "Hard-coded resolution of syntax error",
                            "Introduced logical error from resolution of syntax error",
                            "Resolved syntax error by changing syntax of erroneous component",
                            "Correctly resolved runtime error",
                            "Hard-coded resolution of runtime error",
                            "Introduced logical error from resolution of runtime error",
                            "Correctly resolved type error",
                            "Hard-coded resolution of type error",
                            "Correctly resolved logical error after a single successful run",
                            "Correctly resolved logical error after repeated successful runs", 
                            "Correctly resolved logical error while code not running",
                            "Hard-coded resolution of logical error"]
    return filter_participants_with_codes(resolved_error_codes)

def filter_students_who_resolved_logical_error_while_code_not_running(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantids for participants who resolved a logical error while their code wasn't successfully executing.
    
    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who resolved a logical error while their code wasn't successfully executing.
    """
    return filter_participants_with_codes(["Corrected logical error while code not running"])

"""Filter by program logs introduced and resolved errors"""

def filter_program_logs_who_introduced_syntax_errors(**kwargs) -> dict[str, list[str]]:
    """Filters program logs who introduced an additional syntax error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal syntax error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_id') who introduced a syntax error.
    """
    introduced_syntax_error_codes = ["Addition of non-language-specific strings",
                                    "Incorrect syntactical changes involving fusion or distribution of multiple lines of code",
                                    "Incorrect syntactical changes involving iteration",
                                    "Incorrect syntactical changes involving other statements in program",
                                    "Incorrect syntactical changes involving selection",
                                    "Incorrect syntactical changes involving variable references",
                                    "Incorrect syntactical changes to logical operators",
                                    "Incorrect syntactical changes to mathematical operators",
                                    "Incorrect syntactical changes to other symbols",
                                    "Incorrect syntactical changes to output statements",
                                    "Incorrect syntactical changes to variable assignments",
                                    "Incorrect syntactical changes to whitespace of program"]
    return filter_program_logs_with_codes(introduced_syntax_error_codes)

def filter_students_who_added_and_did_not_resolve_syntax_errors(**kwargs) -> dict[str, list[str]]:
    """Filters program logs that added at least one syntax error and did not resolve an error, using a list of codes associated with introducing/resolving syntax errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_id') who resolved a syntax error.
    """
    introduced_syntax_error_codes = ["Addition of non-language-specific strings",
                                "Incorrect syntactical changes involving fusion or distribution of multiple lines of code",
                                "Incorrect syntactical changes involving iteration",
                                "Incorrect syntactical changes involving other statements in program",
                                "Incorrect syntactical changes involving selection",
                                "Incorrect syntactical changes involving variable references",
                                "Incorrect syntactical changes to logical operators",
                                "Incorrect syntactical changes to mathematical operators",
                                "Incorrect syntactical changes to other symbols",
                                "Incorrect syntactical changes to output statements",
                                "Incorrect syntactical changes to variable assignments",
                                "Incorrect syntactical changes to whitespace of program"]

    resolved_syntax_error_codes = ["Correctly resolved syntax error",
                                "Hard-coded resolution of syntax error",
                                "Introduced logical error from resolution of syntax error",
                                "Resolved syntax error by changing syntax of erroneous component"]
    return filter_program_logs_with_codes(introduced_syntax_error_codes, resolved_syntax_error_codes)

def filter_program_logs_who_introduced_runtime_errors(**kwargs) -> dict[str, list[str]]:
    """Filters program logs who introduced an additional runtime error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal runtime error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_id') who introduced a runtime error.
    """
    introduced_runtime_error_codes = ["Incorrect semantic changes to other statements in program",
                                    "Incorrect semantic changes to variable assignments",
                                    "Incorrect semantic changes to variable references"]
    return filter_program_logs_with_codes(introduced_runtime_error_codes)

def filter_program_logs_who_introduced_type_errors(**kwargs) -> dict[str, list[str]]:
    """Filters program logs who introduced an additional type error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal type error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_id') who introduced a type error.
    """
    introduced_type_error_codes = [ "Incorrect typewise changes involving variables",
                                    "Incorrect typewise changes to function call",
                                    "Incorrect typewise changes to other statements in program"]
    return filter_program_logs_with_codes(introduced_type_error_codes)

def filter_program_logs_who_introduced_logical_errors(**kwargs) -> dict[str, list[str]]:
    """Filters students who introduced an additional logical error in at least one of their attempted exercises, using a list of codes associated with introducing an additonal logical error

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_ids') who introduced a logical error.
    """
    introduced_logical_error_codes = ["Logically incorrect changes involving output statements",
                                    "Logically incorrect changes involving variables",
                                    "Logically incorrect changes to logical operators",
                                    "Logically incorrect changes to mathematical operators",
                                    "Logically incorrect changes to other statements",
                                    "Logically incorrect changes to program flow",
                                    "Introduced logical error from resolution of runtime error",
                                    "Introduced logical error from resolution of syntax error"]
    return filter_program_logs_with_codes(introduced_logical_error_codes)

def filter_program_logs_who_introduced_any_error(**kwargs) -> dict[str, list[str]]:
    """Filters program logs who introduced at least one error in at least one of their attempted exercises, using a list of codes associated with introducing errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_id') who introduced an error.
    """
    introduced_error_codes = ["Addition of non-language-specific strings",
                              "Incorrect syntactical changes involving fusion or distribution of multiple lines of code",
                              "Incorrect syntactical changes involving other statements in program",
                              "Incorrect syntactical changes involving selection",
                              "Incorrect syntactical changes involving variable references",
                              "Incorrect syntactical changes to logical operators",
                              "Incorrect syntactical changes to mathematical operators",
                              "Incorrect syntactical changes to other symbols",
                              "Incorrect syntactical changes to output statements",
                              "Incorrect syntactical changes to variable assignments",
                              "Incorrect syntactical changes to whitespace of program",
                              "Incorrect semantic changes to other statements in program",
                              "Incorrect semantic changes to variable assignments",
                              "Incorrect semantic changes to variable references",
                              "Incorrect typewise changes involving variables",
                              "Incorrect typewise changes to function call",
                              "Incorrect typewise changes to other statements in program",
                              "Logically incorrect changes involving output statements",
                              "Logically incorrect changes involving variables",
                              "Logically incorrect changes to logical operators",
                              "Logically incorrect changes to mathematical operators",
                              "Logically incorrect changes to other statements",
                              "Logically incorrect changes to program flow",
                              "Introduced logical error from resolution of runtime error",
                              "Introduced logical error from resolution of syntax error"]
    return filter_program_logs_with_codes(introduced_error_codes)

def filter_program_logs_who_resolved_any_error(**kwargs) -> dict[str, list[str]]:
    """Filters program logs who resolved at least one error in at least one of their attempted exercises, using a list of codes associated with resolving errors

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_id') who resolved an error.
    """
    resolved_error_codes = ["Correctly resolved syntax error",
                            "Hard-coded resolution of syntax error",
                            "Introduced logical error from resolution of syntax error",
                            "Resolved syntax error by changing syntax of erroneous component",
                            "Correctly resolved runtime error",
                            "Hard-coded resolution of runtime error",
                            "Introduced logical error from resolution of runtime error",
                            "Correctly resolved type error",
                            "Hard-coded resolution of type error",
                            "Correctly resolved logical error after a single successful run",
                            "Correctly resolved logical error after repeated successful runs", 
                            "Correctly resolved logical error while code not running",
                            "Hard-coded resolution of logical error"]
    return filter_program_logs_with_codes(resolved_error_codes)

def filter_program_logs_who_made_any_inconsequential_change(**kwargs) -> dict[str, list[str]]:
    """Filters program logs who made at least one inconsequential change in at least one of their attempted exercises, using a list of codes associated with inconsequential changes

    Returns:
        dict[str, list[str]]: A dictionary containing a list of program_log_ids (under the key 'program_log_id') who made an inconsequential change.
    """
    inconsequential_changes_codes = ["Addition/removal or editing of comments",
                                     "Inconsequential changes involving symbols",
                                     "Inconsequential changes to variable references",
                                     "Inconsequential changes to whitespace of program",
                                     "Inconsequential changes to (existing) outputs",
                                     "Inconsequential changes to (existing) inputs",
                                     "Inconsequential changes to (existing) other statements",
                                     "Addition of unnecessary code"]
    return filter_program_logs_with_codes(inconsequential_changes_codes)

"""Filter based on behaviours exhibited"""

def filter_students_who_ran_before_changes(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantids for participants who ran the code before making changes on each of their attempted exercises.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who ran the code before making changes on each of their attempted exercises.
    """
    return filter_participants_with_codes(["Ran code before making changes"],["Made changes before running code"])

def filter_students_who_changed_before_ran(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantids for participants who made changes before running the code for each of their attempted exercises.
    
    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who made changes before running the code for each of their attempted exercises.
    """
    return filter_participants_with_codes(["Made changes before running code"], ["Ran code before making changes"])

def filter_students_who_made_inconsequential_changes(**kwargs) -> dict[str, list[str]]:
    """Filters students who made at least one inconsequential change in at least one of their attempted exercises, using a list of codes associated with inconsequential changes

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who made an inconsequential change.
    """

    inconsequential_change_codes = ["Addition of unnecessary code", 
                                    "Addition/removal or editing of comments",
                                    "Inconsequential changes involving symbols",
                                    "Inconsequential changes to (existing) inputs",
                                    "Inconsequential changes to (existing) other statements",
                                    "Inconsequential changes to (existing) outputs",
                                    "Inconsequential changes to variable references",
                                    "Inconsequential changes to whitespace of program"]
    return filter_participants_with_codes(inconsequential_change_codes)

def filter_students_who_made_shortcut_changes(**kwargs) -> dict[str, list[str]]:
    """Filters students who made at least one shortcut change (resolved an error by introducing a logical error) in at least one of their attempted exercises, using a list of codes associated with shortcut changes

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who made a shortcut change.
    """
    shortcut_change_codes = ["Introduced logical error from resolution of runtime error",
                             "Introduced logical error from resolution of syntax error"]
    return filter_participants_with_codes(shortcut_change_codes)

def filter_students_who_reverted_previous_changes(**kwargs) -> dict[str, list[str]]:
    """Gets the list of participantids for participants who reverted previous changes in at least one of their attempted exercises.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who reverted a previous change.
    """
    return filter_participants_with_codes(["Reverted previous changes"])

def filter_program_logs_that_ran_before_changes(**kwargs) -> dict[str, list[str]]:
    """Gets the list of programlogids for logs that were ran before changes were made.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of programlogids (under the key 'programlogids') that ran before changes were made.
    """
    return filter_program_logs_with_codes(["Ran code before making changes"],["Made changes before running code"])

def filter_program_logs_that_made_changes_before_running(**kwargs) -> dict[str, list[str]]:
    """Gets the list of programlogids for logs for which changes were made before running.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of programlogids (under the key 'programlogids') that made changes before running.
    """
    return filter_program_logs_with_codes(["Made changes before running code"], ["Ran code before making changes"])

def filter_program_logs_with_reverting_changes(**kwargs) -> dict[str, list[str]]:
    """Gets the list of programLogIds that have the "reverted previous change" associated with them.

    Returns:
        dict[str, list[str]]: A dictionary containing a list of programlogids (under the key 'programlogids') that have reverted previous changes.
    """
    return filter_program_logs_with_codes(["Reverted previous changes"])

"""More functions to generate:
-Average time that students were in error state
-Number of runs with syntax/runtime errors (think I've already got this)
-Number of students who never got program compiling

"""