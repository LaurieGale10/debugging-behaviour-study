from analysis.filter_functions import *
from analysis.stats_helper_functions import *
from Levenshtein import distance

"""Totals functions"""
def length_of_participants_list(*, filtered_ids: dict[str, list[str]], **kwargs) -> int:
    """Function that simply returns the length of a list of participant ids ie how many participants demonstrated a certain behaviour

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        int: The length of the list corresponding to the participantid key in the filtered_ids dictionary
    """
    return len(filtered_ids["participantids"]) if "participantids" in filtered_ids else None

def length_of_program_logs_list(*, filtered_ids: dict[str, list[str]], **kwargs) -> int:
    """Function that simply returns the length of a list of programLogIds ie how many program logs demonstrated a certain behaviour

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        int: The length of the list corresponding to the programlogsid key in the filtered_ids dictionary
    """
    return len(filtered_ids["programlogids"]) if "programlogids" in filtered_ids else None

def total_number_of_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[int]:
    """Function to calculate the total number of runs for a given list of participants or program logs

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[int]: A list containing the total number of runs for each attempted exercise
    """
    total_runs_per_exercises = [0, 0, 0, 0, 0, 0]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        number_runs = len(snapshots) - 1
        total_runs_per_exercises[program_log["exercise_number"] - 1] += number_runs
        total_runs_per_exercises[5] += number_runs
    return total_runs_per_exercises

def get_number_exercises_in_error_state_for_every_run(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the list of programLogIds that have not had any successful runs in their attempts.

    Returns:
        list[list[int]]: The number of attempted exercises that have not had any successful runs in their attempts.
    """
    totals_per_exercises = [0, 0, 0, 0, 0, 0]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            #If every snapshot is in an error state,
            error_state_for_every_run = True
            for i in range(1, len(snapshots)):
                if snapshots[i]["compiled"]:
                    error_state_for_every_run = False
            if error_state_for_every_run:
                totals_per_exercises[program_log["exercise_number"] - 1] += 1
                totals_per_exercises[5] += 1
    return totals_per_exercises

"""Temporal statistics"""

def get_time_on_exercises(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[float]]:
    """Calculates the length of time spent on each attempted exercise by each participant in a given list (discounts exercises that students did not attempt)

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[float]]: A list containing the time spent per attempted exercise, grouped by exercise number
    """
    total_times_per_exercises = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        first_run = snapshots[0]["timestamp"]
        last_run = snapshots[len(snapshots) - 1]["timestamp"]
        if (last_run > first_run):
            time_on_exercise = (last_run - first_run) / 1000
            total_times_per_exercises[program_log["exercise_number"] - 1].append(time_on_exercise)
            total_times_per_exercises[5].append(time_on_exercise)
    return total_times_per_exercises

def get_first_run_time(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[float]]:
    """Calculates the length of time spent on each exercise by each participant in a given list

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[float]]: A list containing the first run time of each attempted exercise, grouped by exercise number
    """
    first_run_times_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            first_run_time = (snapshots[1]["timestamp"] - snapshots[0]["timestamp"]) / 1000
            first_run_times_per_exercise[program_log["exercise_number"] - 1].append(first_run_time)
            first_run_times_per_exercise[5].append(first_run_time)
    return first_run_times_per_exercise

def get_time_between_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the average amount of time between each run for a given list of participants or progam logs

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the time between each runs (changed or unchanged) for each attempted exercise, grouped by exercise number
    """
    time_between_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                time_between_runs = (snapshots[i]["timestamp"] - snapshots[i - 1]["timestamp"]) / 1000
                time_between_runs_per_exercise[program_log["exercise_number"] - 1].append(time_between_runs)
                time_between_runs_per_exercise[5].append(time_between_runs)
    return time_between_runs_per_exercise

def get_time_between_all_unchanged_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the average amount of time between each unchanged run for a given list of participants or progam logs

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the time between unchanged runs (successful and unsuccessful) for each attempted exercise, grouped by exercise number
    """
    unchanged_time_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if (snapshots[i]["snapshot"] == snapshots[i-1]["snapshot"]):
                    time_between_unchanged_runs = (snapshots[i]["timestamp"] - snapshots[i - 1]["timestamp"]) / 1000
                    unchanged_time_runs_per_exercise[program_log["exercise_number"] - 1].append(time_between_unchanged_runs)
                    unchanged_time_runs_per_exercise[5].append(time_between_unchanged_runs)
    return unchanged_time_runs_per_exercise

def get_time_between_successful_unchanged_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the average amount of time between each successful unchanged run for a given list of participants or progam logs

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the time between successful unchanged runs for each attempted exercise, grouped by exercise number
    """
    unchanged_time_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if (snapshots[i]["snapshot"] == snapshots[i-1]["snapshot"] and snapshots[i]["compiled"]):
                    time_between_unchanged_runs = (snapshots[i]["timestamp"] - snapshots[i - 1]["timestamp"]) / 1000
                    unchanged_time_runs_per_exercise[program_log["exercise_number"] - 1].append(time_between_unchanged_runs)
                    unchanged_time_runs_per_exercise[5].append(time_between_unchanged_runs)
    return unchanged_time_runs_per_exercise

def get_time_between_unsuccessful_unchanged_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the average amount of time between each unsuccessful unchanged run for a given list of participants or progam logs

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the time between unsuccessful unchanged runs for each attempted exercise, grouped by exercise number
    """
    unchanged_time_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if (snapshots[i]["snapshot"] == snapshots[i-1]["snapshot"] and not snapshots[i]["compiled"]):
                    time_between_unchanged_runs = (snapshots[i]["timestamp"] - snapshots[i - 1]["timestamp"]) / 1000
                    unchanged_time_runs_per_exercise[program_log["exercise_number"] - 1].append(time_between_unchanged_runs)
                    unchanged_time_runs_per_exercise[5].append(time_between_unchanged_runs)
    return unchanged_time_runs_per_exercise

def get_total_time_in_error_state(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the total time that each attempted exercise was not running for given a list of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the total time each attempted exercise was in an error state, grouped by exercise number
    """
    time_in_error_state_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        time_in_error_state_for_exercise = 0
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(0, len(snapshots) - 1):
                if not snapshots[i]["compiled"]:
                    time_in_error_state_for_exercise += (snapshots[i + 1]["timestamp"] - snapshots[i]["timestamp"]) / 1000
            time_in_error_state_per_exercise[program_log["exercise_number"] - 1].append(time_in_error_state_for_exercise)
            time_in_error_state_per_exercise[5].append(time_in_error_state_for_exercise)
    return time_in_error_state_per_exercise

def get_total_time_in_specific_error_state(*, filtered_ids: dict[str, list[str]], error_type: str, **kwargs) -> list[list[int]]:
    """Gets the total time that a program is in an error state of a particular type (syntax, runtime, type), as derived by the error message

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by
        error_type (str): The type of error: Must be either syntax, runtime, or type error, otherwise an exception is raised

    Returns:
        list[list[int]]: A list of the times that a program is in a particular error state for, per exercise 
    """
    time_in_error_state_per_exercise = [[], [], [], [], [], []]
    error_types_to_message = {
        "syntax": ["SyntaxError"],
        "runtime": ["ValueError, NameError"],
        "type": ["TypeError"]
    }
    if error_type not in error_types_to_message:
        raise ValueError("Not a valid error type")
    
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        time_in_error_state_for_exercise = 0
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                #If snapshot doesn't run and the error message contains one of the items in the list corresponding to the error_type parameter in the error_types_to_message dictionary
                if not snapshots[i]["compiled"] and any(error_type in snapshots[i]["error"]["error"] for error_type in error_types_to_message[error_type]):
                    time_in_error_state_for_exercise += (snapshots[i]["timestamp"] - snapshots[i-1]["timestamp"]) / 1000
            time_in_error_state_per_exercise[program_log["exercise_number"] - 1].append(time_in_error_state_for_exercise)
            time_in_error_state_per_exercise[5].append(time_in_error_state_for_exercise)
    return time_in_error_state_per_exercise

def get_total_running_time(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the total time that each attempted exercise was (successfully) running (compiled == true) for given a list of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the total running time for each attempted exercise, grouped by exercise number
    """
    time_in_running_state_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        time_in_running_state_for_exercise = 0
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(0, len(snapshots) - 1):
                if snapshots[i]["compiled"]:
                    time_in_running_state_for_exercise += (snapshots[i + 1]["timestamp"] - snapshots[i]["timestamp"]) / 1000
            time_in_running_state_per_exercise[program_log["exercise_number"] - 1].append(time_in_running_state_for_exercise)
            time_in_running_state_per_exercise[5].append(time_in_running_state_for_exercise)
    return time_in_running_state_per_exercise

def get_runs_per_minute(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[float]]:
    """Gets the standardised runs per minute statistic for exercise attempted be a given list of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the runs per minute for each attempted exercise, grouped by exercise number
    """
    runs_per_minute_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        number_of_runs_for_snapshot = len(snapshots) - 1
        total_run_time_for_snapshot = (snapshots[number_of_runs_for_snapshot]["timestamp"] - snapshots[0]["timestamp"]) / 1000
        if number_of_runs_for_snapshot > 0 and total_run_time_for_snapshot > 0:
            runs_per_minute_for_snapshot = number_of_runs_for_snapshot / (total_run_time_for_snapshot / 60)
            runs_per_minute_per_exercise[program_log["exercise_number"] - 1].append(runs_per_minute_for_snapshot)
            runs_per_minute_per_exercise[5].append(runs_per_minute_for_snapshot)
    return runs_per_minute_per_exercise

"""Number of runs statistics"""

def get_number_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Calculates the number of runs for each exercise attempted by a given list of participantids

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the total number of runs for each attempted exercise, grouped by exercise number
    """
    number_of_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        number_of_runs_for_snapshot = len(snapshots) - 1
        if number_of_runs_for_snapshot > 0:
            number_of_runs_per_exercise[program_log["exercise_number"] - 1].append(int(number_of_runs_for_snapshot))
            number_of_runs_per_exercise[5].append(int(number_of_runs_for_snapshot))
    return number_of_runs_per_exercise  

def get_number_unsuccessful_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the number of unsuccessful runs for each exercise attempted by a given list of participantids

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the number of unsuccessful runs for each attempted exercise, grouped by exercise number
    """
    number_of_unsuccessful_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) - 1 > 0: #Ensures only attempted exercises are counted
            number_of_unsuccessful_runs_for_snapshot = len([snapshot for snapshot in snapshots if not snapshot["compiled"]]) - 1
            number_of_unsuccessful_runs_per_exercise[program_log["exercise_number"] - 1].append(number_of_unsuccessful_runs_for_snapshot)
            number_of_unsuccessful_runs_per_exercise[5].append(number_of_unsuccessful_runs_for_snapshot)
    return number_of_unsuccessful_runs_per_exercise
        
def get_number_unchanged_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the number of runs that are identical to the previous runs for each exercise attempted by a given ist of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the number of unchanged runs (either successful or unsuccessful) for each attempted exercise, grouped by exercise number
    """
    number_unchanged_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        number_unchanged_runs_for_snapshot = 0
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if (snapshots[i]["snapshot"] == snapshots[i-1]["snapshot"]):
                    number_unchanged_runs_for_snapshot += 1
            number_unchanged_runs_per_exercise[program_log["exercise_number"] - 1].append(number_unchanged_runs_for_snapshot)
            number_unchanged_runs_per_exercise[5].append(number_unchanged_runs_for_snapshot)
    return number_unchanged_runs_per_exercise

def get_number_unchanged_successful_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the number of runs that are identical to the previous runs for each exercise attempted by a given list of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the number of successful unchanged runs for each attempted exercise, grouped by exercise number
    """
    number_unchanged_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        number_unchanged_runs_for_snapshot = 0
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if snapshots[i]["snapshot"] == snapshots[i-1]["snapshot"] and snapshots[i]["compiled"]:
                    number_unchanged_runs_for_snapshot += 1
            number_unchanged_runs_per_exercise[program_log["exercise_number"] - 1].append(number_unchanged_runs_for_snapshot)
            number_unchanged_runs_per_exercise[5].append(number_unchanged_runs_for_snapshot)
    return number_unchanged_runs_per_exercise

def get_number_unchanged_unsuccessful_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the number of runs that are identical to the previous runs for each exercise attempted by a given list of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the number of unsuccessful unchanged runs for each attempted exercise, grouped by exercise number
    """
    number_unchanged_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        number_unchanged_runs_for_snapshot = 0
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if snapshots[i]["snapshot"] == snapshots[i-1]["snapshot"] and not snapshots[i]["compiled"]:
                    number_unchanged_runs_for_snapshot += 1
            number_unchanged_runs_per_exercise[program_log["exercise_number"] - 1].append(number_unchanged_runs_for_snapshot)
            number_unchanged_runs_per_exercise[5].append(number_unchanged_runs_for_snapshot)
    return number_unchanged_runs_per_exercise

def get_number_successful_snapshots_after_given_run(*, filtered_ids: dict[str, list[str]], run_number: int, **kwargs) -> list[int]:
    """Calculates the total number of snapshots that were successfully running after a given number of runs

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by
        run_number (int): The run number to check each snapshot at. If the run number is greater than the total number of runs for a given snapshot, the snapshot's data cannot be included in the list.

    Returns:
        list[list[int]]: A list of the number of programs successfully running after run_number runs, per exercise 
    """
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)

    if run_number <= 0:
        raise ValueError("Cannot select a run number less than or equal to 0")
    total_snapshots = [0, 0, 0, 0, 0, 0]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) >= run_number:
            if snapshots[run_number]["compiled"]:
                total_snapshots[program_log["exercise_number"] - 1] += 1
                total_snapshots[5] += 1
    return total_snapshots

def get_number_unsuccessful_snapshots_after_given_run(*, filtered_ids: dict[str, list[str]], run_number: int, **kwargs) -> list[int]:
    """Calculates the total number of snapshots that were not successfully running after a given number of runs

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by
        run_number (int): The run number to check each snapshot at. If the run number is greater than the total number of runs for a given snapshot, the snapshot's data cannot be included in the list.

    Returns:
        list[list[int]]: A list of the number of programs not successfully running after run_number runs, per exercise 
    """
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)

    if run_number <= 0:
        raise ValueError("Cannot select a run number less than or equal to 0")
    total_snapshots = [0, 0, 0, 0, 0, 0]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) >= run_number:
            if not snapshots[run_number]["compiled"]:
                total_snapshots[program_log["exercise_number"] - 1] += 1
                total_snapshots[5] += 1
    return total_snapshots

def get_number_changed_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Gets the number of runs that are identical to the previous runs for each exercise attempted by a given list of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the number of changed runs for each attempted exercise, grouped by exercise number
    """
    number_changed_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        number_unchanged_runs_for_snapshot = 0
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if (snapshots[i]["snapshot"] != snapshots[i-1]["snapshot"]):
                    number_unchanged_runs_for_snapshot += 1
            number_changed_runs_per_exercise[program_log["exercise_number"] - 1].append(number_unchanged_runs_for_snapshot)
            number_changed_runs_per_exercise[5].append(number_unchanged_runs_for_snapshot)
    return number_changed_runs_per_exercise

"""Edit distance statistics"""

def get_edit_distance_between_changed_runs(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Calculates the average Levenshtein edit distance between the changed runs of the attempted exercises of a given set of participants i.e. given a student has made a change between runs, how big is it
    Identical pairs of runs (possessing an edit distance of 0) are discounted from this

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the edit distance between (changed runs) for each attempted exercise, grouped by exercise number
    """
    unchanged_time_runs_per_exercise = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if (snapshots[i]["snapshot"] != snapshots[i-1]["snapshot"]):
                    edit_distance = distance(snapshots[i]["snapshot"], snapshots[i-1]["snapshot"])
                    if edit_distance > 0:
                        unchanged_time_runs_per_exercise[program_log["exercise_number"] - 1].append(edit_distance)
                        unchanged_time_runs_per_exercise[5].append(edit_distance)
    return unchanged_time_runs_per_exercise

def get_edit_distance_between_first_and_last_snapshot(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Calculates the edit distance between the original and end state of students' snapshots for a given list of participantids or programlogids

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the edit distance between the first and last run for each attempted exercise, grouped by exercise number
    """
    edit_distances_between_exercises = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            edit_distance = distance(snapshots[len(snapshots) - 1]["snapshot"], snapshots[0]["snapshot"])
            edit_distances_between_exercises[program_log["exercise_number"] - 1].append(edit_distance)
            edit_distances_between_exercises[5].append(edit_distance)
    return edit_distances_between_exercises

def get_edit_distance_between_first_snapshot_and_original_program(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[list[int]]:
    """Calculates the edit distance between the original program state and the first snapshot for a given list of participantids or programlogids

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        list[list[int]]: A list containing the edit distance between the original program state and the first snapshot for each attempted exercise, grouped by exercise number
    """
    edit_distances_between_exercises = [[], [], [], [], [], []]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1:
            edit_distance = distance(snapshots[1]["snapshot"], snapshots[0]["snapshot"])
            edit_distances_between_exercises[program_log["exercise_number"] - 1].append(edit_distance)
            edit_distances_between_exercises[5].append(edit_distance)
    return edit_distances_between_exercises

"""These functions are slightly different in what they return; can think of them as terminal"""

def get_end_state_of_program(*, filtered_ids: dict[str, list[str]], **kwargs)  -> dict[str, list[int]]:
    """Gets the end state for each exercise attempted by a given list of participants

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by

    Returns:
        dict[str: list(int)]: Dictionary containing each error type as a key, corresponding to a list of counts for each exercise
    """
    end_state_codes = ["Ended exercise with syntax error(s)", "Ended exercise with runtime error(s)", "Ended exercise with type error(s)", "Ended exercise with logical error(s)", "Ended exercise in correct state", "Didn't attempt exercise"]
    
    distributions_per_exercise = {
        "Ended exercise with syntax error(s)": [0, 0, 0, 0, 0],
        "Ended exercise with runtime error(s)": [0, 0, 0, 0, 0],
        "Ended exercise with type error(s)": [0, 0, 0, 0, 0],
        "Ended exercise with logical error(s)": [0, 0, 0, 0, 0],
        "Ended exercise in correct state": [0, 0, 0, 0, 0],
        "Didn't attempt exercise": [0, 0, 0, 0, 0],
        "Total attempts": [0, 0, 0, 0, 0],
    }
    
    program_logs = kwargs["program_logs"]
    coded_program_logs = kwargs["coded_program_logs"]
    #filtered_program_logs is required for getting exercise number for a particular id in filtered_program_log_ids
    if "participantids" in filtered_ids:
        filtered_program_logs = program_logs[program_logs["participantid"].isin(filtered_ids["participantids"])]
        filtered_program_log_ids = filtered_program_logs["id"].tolist()
    elif "programlogids" in filtered_ids:
        filtered_program_logs = program_logs[program_logs["id"].isin(filtered_ids["programlogids"])]
        filtered_program_log_ids = filtered_ids["programlogids"]
    else:
        filtered_program_logs = program_logs
        filtered_program_log_ids = filtered_program_logs["id"].tolist()
    
    for id in filtered_program_log_ids:
        exercise_number = filtered_program_logs[filtered_program_logs["id"] == id]["exercise_number"].item()
        filtered_coded_program_logs = coded_program_logs[coded_program_logs["program_log_id"] == id]
        codes = filtered_coded_program_logs[filtered_coded_program_logs["code_name"].isin(end_state_codes)]["code_name"].tolist()
        ##TODO: Fix: not getting 346 as number of attempted exercises
        if codes == [] or codes == None or "Didn't attempt exercise" in codes: #If an exercise hasn't been coded, assumes that it hasn't been attempted
            distributions_per_exercise["Didn't attempt exercise"][exercise_number - 1] += 1
        else:
            for code in codes:
                distributions_per_exercise[code][exercise_number - 1] += 1
            distributions_per_exercise["Total attempts"][exercise_number - 1] += 1
    return distributions_per_exercise

def get_number_attempted_exercises(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[int]:
    attempted_exercises = [0, 0, 0, 0, 0, 0]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if len(snapshots) > 1 and snapshots[0]["snapshot"] != snapshots[len(snapshots) - 1]["snapshot"]:
            attempted_exercises[program_log["exercise_number"] - 1] += 1
            attempted_exercises[5] += 1
    return attempted_exercises

def get_number_unattempted_exercises(*, filtered_ids: dict[str, list[str]], **kwargs) -> list[int]:
    """Gets the number of unattempted exercises for a given set of participants and program logs. That is, exercises where every run is identical

    Args:
        filtered_ids (dict[str, list[str]]): The list of participantids or programlogids to filter by
    
    Returns:
        list[list[int]]: A list containing the number of unattempted exercises, grouped by exercise number
    """
    unattempted_exercises = [0, 0, 0, 0, 0, 0]
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    for index, program_log in filtered_program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        all_runs_identical = True
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if snapshots[i]["snapshot"] != snapshots[i-1]["snapshot"]:
                    all_runs_identical = False
                    break
        if all_runs_identical:
            unattempted_exercises[program_log["exercise_number"] - 1] += 1
            unattempted_exercises[5] += 1
    return unattempted_exercises

"""Paper-specific stats"""

def number_students_first_change_same_as_student_19_exercise_1(**kwargs) -> int:
    """Gets the number of students who made the same number of change

    Returns:
        int: A count of the number of students whose first change on exercise 1 is the same as student 19's
    """
    string_to_compare = "# Question 1\nheight = depth\nwidth = 50\ndepth = 25\nvolume = height * width * depth\nprint(\"The volume is,volume\")" #The first change made by student 14 in exercise 1
    count = 0
    program_logs = kwargs["program_logs"]
    for index, program_log in program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if program_log["exercise_number"] == 1 and len(snapshots) > 1:
            first_change_index = 1 #Gets the run number that the first change was made on (not guaranteed to the be the first run)
            while first_change_index < len(snapshots)-1 and snapshots[first_change_index]["snapshot"] == snapshots[0]["snapshot"]:
                first_change_index += 1
            if snapshots[first_change_index]["snapshot"] == string_to_compare:
                count += 1
    return count

def number_students_unsuccessful_first_change_exercise_4(**kwargs) -> int:
    """Gets the number of students who made a non-corrective change to line 4 of exercise 4 in their first run.

    Returns:
        int: A count of the number of students whose first change on exercise 1 is the same as student 19's
    """
    count = 0
    original_state = "while count<12:"
    program_logs = kwargs["program_logs"]
    for index, program_log in program_logs.iterrows():
        snapshots = program_log["logs_snapshots"]
        if program_log["exercise_number"] == 4 and len(snapshots) > 2 and snapshots[1]["snapshot"] == snapshots[0]["snapshot"]:
            first_change_index = 2
            #Gets the run where the initial change to an exercise was made (not guaranteed to the be the first run) - iterate until the snapshot for a given run is not equal to the original program state
            while first_change_index < len(snapshots)-1 and snapshots[first_change_index]["snapshot"] == snapshots[0]["snapshot"]:
                first_change_index += 1
            edited_state = snapshots[first_change_index]["snapshot"]
            if len(edited_state.splitlines()) >= 4 and edited_state.splitlines()[3] != original_state and not snapshots[first_change_index]["compiled"]:
                count += 1
    return count