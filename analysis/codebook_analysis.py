import csv
import json
from pathlib import Path
from analysis.core_filter_functions import *
from analysis.stats_functions import *

old_codebook: list[str] = ["First move",
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

def load_codebook() -> list:
    """Load and basic-validate the project's codebook JSON file.
    """
    # Use current working directory to locate the codebook JSON
    path = Path.cwd() / "analysis" / "codebook.json"
    with open(path, encoding="utf-8") as fh:
        codebook = json.load(fh)
    #Do any parsing?
    return codebook

def save_code_counts():
    """Records and saves the count of each code (in terms of program logs and number of students who demonstrate the code) to a csv
    """
    codebook = load_codebook()
    N_PARTICIPANTS: int = 73
    N_ATTEMPTS: int = 322

    def get_descendant_leaf_labels(node: dict):
        """Return a list of labels for all descendant leaf nodes under `node`.

        A leaf is defined as a node that does not have a 'children' list.
        """
        labels = []
        # node expected to be a dict with 'label' and optional 'children'
        children = node.get("children")
        if not children:
            # leaf
            labels.append(node.get("label"))
        else:
            for child in children:
                labels.extend(get_descendant_leaf_labels(child))
        return labels

    def write_node(writer, node, depth=0):
        label = node.get("label")
        descendant_labels = get_descendant_leaf_labels(node)

        if descendant_labels != []:
            n_participants_with_code: int = length_of_participants_list(filtered_ids=filter_participants_with_codes(descendant_labels))
            n_program_logs_with_code: int = length_of_program_logs_list(filtered_ids=filter_program_logs_with_codes(descendant_labels))
        else:
            n_participants_with_code: int = length_of_participants_list(filtered_ids=filter_participants_with_codes([label]))
            n_program_logs_with_code: int = length_of_program_logs_list(filtered_ids=filter_program_logs_with_codes([label]))

        pct_participants = round((n_participants_with_code / N_PARTICIPANTS) * 100, 2) if N_PARTICIPANTS else 0
        pct_attempts = round((n_program_logs_with_code / N_ATTEMPTS) * 100, 2) if N_ATTEMPTS else 0

        writer.writerow([
            "\t" * depth + label,
            n_participants_with_code,
            pct_participants,
            n_program_logs_with_code,
            pct_attempts,
        ])

        # recurse into children (if any)
        if isinstance(node, dict):
            for child in node.get("children", []):
                write_node(writer, child, depth + 1)

    with open("results/codebook_frequency.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["label", "n_participants", "pct_participants", "n_exercise_attempts", "pct_exercise_attempts"])
        for node in codebook:
            write_node(writer, node, depth=0)
