from pandas import DataFrame
import numpy as np
from scipy.stats import skew

def get_filtered_program_logs(*, filtered_ids: dict[str, list[str]], **kwargs) -> DataFrame:
    """Gets the list of program logs based on a list of filtered participantids or programlogids

    Args:
        filtered_ids (dict[str, list[str]]): A dictionary containing referencing either a list of participantids or programlogids to filter by.
        If the dictionary contains neither of these, the whole program logs DataFrame is returned (nothing is filtered)

    Returns:
        DataFrame: Filtered rows of the program_logs table.
    """
    program_logs = kwargs["program_logs"]
    if "participantids" in filtered_ids:
        filtered_program_logs = program_logs[program_logs["participantid"].isin(filtered_ids["participantids"])]
    elif "programlogids" in filtered_ids:
        filtered_program_logs = program_logs[program_logs["id"].isin(filtered_ids["programlogids"])]
    else:
        filtered_program_logs = program_logs
    return filtered_program_logs


def get_uncoded_attempted_runs(**kwargs) -> list[int]:
    """Function to be discarded after analysis. Used to identify which valid exercise attempts haven't currently been coded with anything"""
    all_program_log_ids = set(kwargs["program_logs"]["id"])
    coded_program_log_ids = set(kwargs["coded_program_logs"]["program_log_id"])
    uncoded_program_log_ids = [id for id in all_program_log_ids if id not in coded_program_log_ids]
    return uncoded_program_log_ids


def get_missing_first_run_codes(**kwargs) -> list[int]:
    """Function used to check every attempted exercise has a first run code associated with it"""
    all_program_log_ids = set(kwargs["program_logs"]["id"])
    codes_to_check = []
    coded_program_logs_frame = kwargs["coded_program_logs"]
    for id in all_program_log_ids:
        set_of_codes = coded_program_logs_frame.loc[coded_program_logs_frame["program_log_id"] == id]["code_name"].values.tolist()
        if "Ran code before making changes" not in set_of_codes and "Made changes before running code" not in set_of_codes and "Didn't attempt exercise" not in set_of_codes:
            codes_to_check.append(id)
    return codes_to_check