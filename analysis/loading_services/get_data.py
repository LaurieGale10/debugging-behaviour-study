from pandas import DataFrame
from analysis.loading_services.connection_pool import *

def get_data(table: str) -> DataFrame:
    """Basic starter function that obtains all the data from a given table (including data not used in analysis)"""
    with db_cursor() as cursor:
        if table == "program_logs":
            cursor.execute("SELECT * FROM program_logs WHERE status != 'DNA' ORDER BY (logs_snapshots[jsonb_array_length(logs_snapshots) - 1]['timestamp']::int8 - logs_snapshots[0]['timestamp']::int8) / 1000;")
        else:
            cursor.execute("SELECT * FROM {}".format(table))
        data = DataFrame(cursor.fetchall())
        data.columns = [description[0] for description in cursor.description]
    return data

def filter_null_data(data: DataFrame, table: str) -> DataFrame:
    """Filters the program_logs or participants DataFrames by removing null data based on relevant fields"""
    if table == "program_logs":
        return data[data.status != "DNA"]
    elif table == "participants":
        return data[data.comments != "DNA"]
    return None

def clear_unattempted_exercises(data: DataFrame) -> DataFrame:
    for index, program_log in data.iterrows():
        snapshots = program_log["logs_snapshots"]
        all_runs_identical = True
        if len(snapshots) > 1:
            for i in range(1, len(snapshots)):
                if snapshots[i]["snapshot"] != snapshots[i-1]["snapshot"]:
                    all_runs_identical = False
                    break
        if all_runs_identical:
            data.drop(index, inplace=True)
    return data