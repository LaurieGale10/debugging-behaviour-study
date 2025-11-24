import csv
import json
from pathlib import Path
from analysis.core_filter_functions import *
from analysis.stats_functions import *

N_PARTICIPANTS: int = 73
N_ATTEMPTS: int = 322

def load_codebook() -> list:
    """Load and basic-validate the project's codebook JSON file.
    """
    # Use current working directory to locate the codebook JSON
    path = Path.cwd() / "analysis" / "codebook.json"
    with open(path, encoding="utf-8") as fh:
        codebook = json.load(fh)
    #Do any parsing?
    return codebook

def flatten_codebook_tree(tree: list) -> list:
    """Flatten the nested codebook tree (as returned by create_codebook_with_frequencies)
    into a list of rows suitable for CSV output.
    """
    rows: list[dict] = []

    def _flatten(node: dict):
        rows.append({
            "label": node["label"],
            "depth": node["depth"],
            "n_participants": node["n_participants"],
            "pct_participants": node["pct_participants"],
            "n_exercise_attempts": node["n_exercise_attempts"],
            "pct_exercise_attempts": node["pct_exercise_attempts"],
        })
        for c in node.get("children", []):
            _flatten(c)

    for top in tree:
        _flatten(top)
    return rows

def create_codebook_with_frequencies() -> list:
    """Build a nested codebook (list of dict nodes) that mirrors the JSON codebook
    but includes computed frequency fields at every node.

    Each node in the returned structure contains:
      - label: string
      - depth: int
      - n_participants: int
      - pct_participants: float
      - n_exercise_attempts: int
      - pct_exercise_attempts: float
      - leaf_labels: list[str]  # all descendant leaf labels used for filtering
      - children: list[node]    # same structure recursively

    Returns the top-level list of node dicts.
    """
    codebook = load_codebook()

    def get_descendant_leaf_labels(node: dict) -> list:
        children = node.get("children")
        if not children:
            return [node.get("label")]
        labels = []
        for child in children:
            labels.extend(get_descendant_leaf_labels(child))
        return labels

    def build_node_for_code(node: dict, depth: int = 0) -> dict:
        label = node.get("label")
        leaf_labels = get_descendant_leaf_labels(node)

        participant_ids = filter_participants_with_codes(leaf_labels)
        program_log_ids = filter_program_logs_with_codes(leaf_labels)

        n_participants_with_code = length_of_participants_list(filtered_ids=participant_ids)
        n_program_logs_with_code = length_of_program_logs_list(filtered_ids=program_log_ids)

        pct_participants = round((n_participants_with_code / N_PARTICIPANTS) * 100, 2)
        pct_attempts = round((n_program_logs_with_code / N_ATTEMPTS) * 100, 2)

        built_code = {
            "label": label,
            "depth": depth, #Required for correctly indenting in CSV
            "n_participants": n_participants_with_code,
            "pct_participants": pct_participants,
            "n_exercise_attempts": n_program_logs_with_code,
            "pct_exercise_attempts": pct_attempts,
            "leaf_labels": leaf_labels,
            "children": [],
        }

        for subcode in node.get("children", []):
            built_subcode = build_node_for_code(subcode, depth + 1)
            built_code["children"].append(built_subcode)
        return built_code

    return [build_node_for_code(n, depth=0) for n in codebook]


def save_code_counts():
    """Write the codebook frequencies to CSV using create_codebook_with_frequencies()."""
    codebook_with_frequencies = create_codebook_with_frequencies()
    rows = flatten_codebook_tree(codebook_with_frequencies)
    with open("results/codebook_frequency.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["label", "n_participants", "pct_participants", "n_exercise_attempts", "pct_exercise_attempts"])
        for r in rows:
            label = "\t" * r["depth"] + r["label"]
            writer.writerow([label, r["n_participants"], r["pct_participants"], r["n_exercise_attempts"], r["pct_exercise_attempts"]])

def get_most_frequent_codes(n: int = 10) -> list[tuple[str, int]]:
    """Return the `n` most frequently occurring codes across all program logs.

    Each code is represented as a tuple of (code_label, count).
    """
    # Build the frequency tree and flatten it
    codebook_with_frequencies = create_codebook_with_frequencies()
    rows = flatten_codebook_tree(codebook_with_frequencies)

    sorted_rows = sorted(rows, key=lambda r: r.get("n_exercise_attempts", 0), reverse=True)
    return [(r["label"], r["n_exercise_attempts"]) for r in sorted_rows[:n]]

def get_most_frequent_bottom_level_codes_per_exercise_attempt(n: int = 15) -> list[tuple[str, int]]:
    """Return the `n` most frequently occurring bottom-level codes across all program logs.

    Each code is represented as a tuple of (code_label, count).
    """
    codebook_with_frequencies = create_codebook_with_frequencies()
    bottom_level_codes: list[tuple[str, int]] = []

    def _collect_bottom_level_codes(node: dict):
        if not node.get("children"):
            bottom_level_codes.append((node.get("label"), node.get("n_exercise_attempts", 0)))
        else:
            for c in node.get("children", []):
                _collect_bottom_level_codes(c)

    for top in codebook_with_frequencies:
        _collect_bottom_level_codes(top)

    # Sort leaf rows by count descending and return top n
    sorted_bottom_level_codes = sorted(bottom_level_codes, key=lambda t: t[1], reverse=True)
    return sorted_bottom_level_codes[:n]

def get_most_frequent_bottom_level_codes_per_participant(n: int = 15) -> list[tuple[str, int]]:
    """Return the `n` most frequently occurring bottom-level codes across all participants.

    Each code is represented as a tuple of (code_label, count).
    """
    codebook_with_frequencies = create_codebook_with_frequencies()
    bottom_level_codes: list[tuple[str, int]] = []

    def _collect_bottom_level_codes(node: dict):
        if not node.get("children"):
            bottom_level_codes.append((node.get("label"), node.get("n_participants", 0)))
        else:
            for c in node.get("children", []):
                _collect_bottom_level_codes(c)

    for top in codebook_with_frequencies:
        _collect_bottom_level_codes(top)

    # Sort leaf rows by count descending and return top n
    sorted_bottom_level_codes = sorted(bottom_level_codes, key=lambda t: t[1], reverse=True)
    return sorted_bottom_level_codes[:n]