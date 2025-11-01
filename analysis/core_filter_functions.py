from pandas import DataFrame
from analysis.loading_services import connection_pool


def filter_participants_with_code_in_all_exercises(include_codes : list[str] = [], exclude_codes: list[str] = []) -> dict[str, list[str]]:
    """Returns the list of participants who have a certain code associated with all of their attempted runs

    Args:
        include_codes (list[str], optional): _description_. Defaults to [].
        exclude_codes (list[str], optional): _description_. Defaults to [].

    Returns:
        dict[str, list[str]]: _description_
    """
    pass

def filter_participants_with_codes(include_codes : list[str] = [], exclude_codes: list[str] = []) -> dict[str, list[str]]:
    """ Gets the list of participants who have a certain code associated with at least one of their attempted runs

    Args:
        include_codes (list[str], optional): Codes to students must have assigned to at least one of their attempted exercises. Defaults to [].
        exclude_codes (list[str], optional): Codes that students must not have assigned to any of their attempted exercise. Defaults to [].

    Returns:
        dict[str, list[str]]: Dictionary containing a list of participantids to filter by
    """
    with connection_pool.db_cursor() as cursor:
        cursor.execute("SELECT DISTINCT participantid FROM program_logs JOIN coded_program_logs ON program_logs.id = coded_program_logs.program_log_id WHERE code_name=ANY(%s::text[]) EXCEPT SELECT DISTINCT participantid FROM program_logs JOIN coded_program_logs ON program_logs.id = coded_program_logs.program_log_id WHERE code_name=ANY(%s::text[]) ORDER BY participantid;",
                    (include_codes, exclude_codes))

        participants_with_code = DataFrame(cursor.fetchall())
        if participants_with_code.empty:
            return {}
        filtered_id_dict = {}
        participants_with_code.columns = [description[0] for description in cursor.description]
        participant_ids = participants_with_code["participantid"].values.tolist()
        filtered_id_dict["participantids"] = participant_ids
    return filtered_id_dict

def filter_program_logs_with_codes(include_codes : list[str] = [], exclude_codes: list[str] = []) -> dict[str, list[str]]:
    """Returns the list of program logs that have tagged (or not) with a certain set of codes

    Args:
        include_codes (list[str], optional): Codes that attempted exercises must have assigned to them. Defaults to [].
        exclude_codes (list[str], optional): Codes that attempted exercises must not have assigned to them. Defaults to [].

    Returns:
        dict[str, list[str]]: Dictionary containing a list of programlogids to filter by
    """
    with connection_pool.db_cursor() as cursor:
        cursor.execute("SELECT DISTINCT program_log_id FROM program_logs JOIN coded_program_logs ON program_logs.id = coded_program_logs.program_log_id WHERE code_name=ANY(%s::text[]) EXCEPT SELECT DISTINCT program_log_id FROM program_logs JOIN coded_program_logs ON program_logs.id = coded_program_logs.program_log_id WHERE code_name=ANY(%s::text[]) ORDER BY program_log_id;",
                    (include_codes, exclude_codes))

        program_logs_with_code = DataFrame(cursor.fetchall())
        if program_logs_with_code.empty:
            return {}
        filtered_id_dict = {}
        program_logs_with_code.columns = [description[0] for description in cursor.description]
        program_log_ids = program_logs_with_code["program_log_id"].values.tolist()
        filtered_id_dict["programlogids"] = program_log_ids
    return filtered_id_dict

#TODO: Change this to filter by list of exercise numbers
def filter_by_exercise_number(exercise_number: int, **kwargs) -> DataFrame:
    """Filters the programs_logs DataFrame by a particular exercise number

    Args:
        exercise_number (int): Exercise number to filter by

    Returns:
        DataFrame: Program_logs DataFrame filtered by exercise_number
    """
    program_logs = kwargs["program_logs"]
    filtered_id_dict = {}
    filtered_program_logs = program_logs.loc[program_logs["exercise_number"] == exercise_number]
    filtered_program_log_ids = filtered_program_logs["id"].values.tolist()
    filtered_id_dict["programlogids"] = filtered_program_log_ids
    return filtered_id_dict

