import loading_services.connection_pool
from pandas import DataFrame
from collections import namedtuple
from Levenshtein import distance

def get_time_run_number_pairings(participantid: str, exercise_number: int) -> list[tuple[float, int, bool, int]]:
    """
    Gets a list of students' runs over time, adding data on outcome of run and edit distance in relation to previous run.

    @param participantid: participantid to get pairings for
    @param exercise_number: exercise number that participant attempted to get pairings for
    @return list of 3-ples providing data about a particular run: (run_number, time_since_first_run, compiled, edit_distance_between_original_run)
    """

    #Get data from DB
    with loading_services.connection_pool.connection_pool.db_cursor() as cursor:
        cursor.execute("SELECT logs_snapshots FROM program_logs WHERE participantid = %s AND exercise_number = %s;",
                    (participantid, exercise_number))
        program_logs = cursor.fetchall()[0][0]

    ##TODO: Exception handling of failed connection pool and if exercise is a duplicate/not attempted
    run_number = 1
    runs = []
    #Adds relevant data to list of 4-ples
    for i in range(1, len(program_logs)):
        time_so_far = (program_logs[i]["timestamp"] - program_logs[0]["timestamp"]) / 1000
        edit_distance = distance(program_logs[i]["snapshot"], program_logs[i-1]["snapshot"])
        runs.append((run_number, time_so_far, program_logs[i]["compiled"], edit_distance))
        run_number += 1
    return runs

def time_on_task(logs_snapshots: list[str]) -> float:
    """Adds the time on task column to a program logs DataFrame. Useful for reusing time_on_task calculations and sorting logs based on time on task

    Args:
        list[str]: JSON object representing program_logs_dataframe["logs_snapshots"]

    Returns:
        float: The time on task for a given exercise attempt
    """
    time_on_task = (logs_snapshots[len(logs_snapshots) - 1]["timestamp"] - logs_snapshots[0]["timestamp"]) / 1000
    return time_on_task

def get_points_data(exercises: DataFrame): 
    exercise_id = 0
        #Creation of point named tuple
    Point = namedtuple("Point", ["exerciseid", "participantid", "exercise_number", "time_since_first_run", "compiled", "edit_distance", "is_unchanged_run"])
    points = []

    for index, attempted_exercise in exercises.iterrows():
        snapshots = attempted_exercise["logs_snapshots"]
        #Iterate through every snapshot and creates additional point
        for i in range(1, len(snapshots)):
            time_since_first_run = (snapshots[i]["timestamp"] - snapshots[0]["timestamp"]) / 1000
            edit_distance = distance(snapshots[i]["snapshot"], snapshots[i-1]["snapshot"])
            is_unchanged_run = snapshots[i]["snapshot"] == snapshots[i-1]["snapshot"]

            points.append(Point(exercise_id, attempted_exercise["participantid"], attempted_exercise["exercise_number"], time_since_first_run, snapshots[i]["compiled"], edit_distance, is_unchanged_run))
        exercise_id += 1
    return points