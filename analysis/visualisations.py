from statistics import median
import matplotlib.pyplot as plt
import numpy as np

from analysis.loading_services.get_data import *
from analysis.stats_functions import get_end_state_of_program
from analysis.stats_helper_functions import get_filtered_program_logs
from log_data_visualisation_helper_functions import *

successful_run_colour = "blue"
unsuccessful_run_colour = "goldenrod"

coded_program_logs = get_data("coded_program_logs") #TODO: Does this need filtering?
codes = get_data("codes")["code_name"].values.tolist()
participants = filter_null_data(get_data("participants"), "participants") #TODO: Currently this returns 90 participants; needs to be exactly 73
program_logs = filter_null_data(get_data("program_logs"),"program_logs")
participants_list = participants['participantid'].values.tolist()

dataframes = {
    "coded_program_logs": coded_program_logs,
    "codes": codes,
    "participants": participants,
    "program_logs": program_logs
}

"""Plots particular visualisations to include in the paper"""

#TODO: Include option to pipe from filter (limit list that is available)
def visualise_progress_over_time(*, filtered_ids: dict[str, list[str]], **kwargs):
    """Plots the progress of some attempted exercise over time, using a line graph and a fill between graph
    """
    fig, ax = plt.subplots()
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Number of active exercise attempts in a state")
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)

    number_unsuccessful_runs_plot = [] #List used to plot the number of changes
    proportion_unsuccessful_runs_plot = [] #List containing values to plot the red line
    number_successful_runs_plot = []
    proportion_successful_runs_plot = [] #List containing values to plot the red line
    number_runs_plot = [] #List containing values to plot the purple line

    time_counter = 0
    time_intervals = []
    time_increment = 1 #Number of seconds to take readings at
    no_exercises_attempted = False #Used if I want to plot ALL of the data rather than limit it based on time

    while time_counter <= 700:
        no_exercises_attempted = True
        #Data related to unsuccessful runs (at a given time point)
        total_unsuccessful_programs = 0
        #Data related to successful runs (at a given time point)
        total_successful_programs = 0
        #Data related to successful runs (at a given time point)
        total_programs = 0
        for index, attempted_exercise in filtered_program_logs.iterrows():
            snapshots = attempted_exercise["logs_snapshots"]
            total_time_on_exercise = (snapshots[len(snapshots) - 1]["timestamp"] - snapshots[0]["timestamp"]) / 1000
            if total_time_on_exercise > time_counter:
                no_exercises_attempted = False
                most_recent_run = [snapshot for snapshot in snapshots if (snapshot["timestamp"] - snapshots[0]["timestamp"]) / 1000 <= time_counter][-1] #The last snapshot the student program at t = time_counter
                most_recent_run_state = most_recent_run["compiled"]
                if most_recent_run_state:
                    total_successful_programs += 1
                else:
                    total_unsuccessful_programs += 1
                total_programs += 1
                proportion_unsuccessful_programs = (total_unsuccessful_programs / (total_unsuccessful_programs + total_successful_programs)) * 100
                proportion_successful_programs = (total_successful_programs / (total_unsuccessful_programs + total_successful_programs)) * 100
        #Add necessary info to appropriate lists
        number_unsuccessful_runs_plot.append(total_unsuccessful_programs)
        proportion_unsuccessful_runs_plot.append(proportion_unsuccessful_programs)
        number_successful_runs_plot.append(total_successful_programs)
        proportion_successful_runs_plot.append(proportion_successful_programs)
        number_runs_plot.append(total_programs)

        #Record and adjust time
        time_intervals.append(time_counter)
        time_counter += time_increment
        
    ax.plot(time_intervals, number_successful_runs_plot, color="g")
    ax.fill_between(time_intervals, number_successful_runs_plot, color="g", alpha = 0.3)
    ax.plot(time_intervals, number_runs_plot, color="r")
    ax.fill_between(time_intervals, number_runs_plot, number_successful_runs_plot, color="r", alpha = 0.3)

    plt.show()

def model_time_over_runs_for_exercises(exercises: list[tuple[str, int]], names: list[str]):
    """Creates a event plot of a list of student's progress on a single attempted exercise.
    x: run number, y: time(seconds) since run 0, colour: outcome of run, thickness of line between points"""
    #Create initial plot
    fig, ax = plt.subplots()
    ax.set_xlabel("Time (seconds)")
    line_offsets = [i * 1.25 for i in range(len(exercises))]
    names_to_offsets = {} #For putting event plots in right locations
    plt.yticks([])
    for i in range(len(exercises)):
        participantid = exercises[i][0]
        names_to_offsets[participantid] = line_offsets[i]

    successful_runs = []
    unsuccessful_runs = []

    #Get necessary data and plot for each participant
    for (participantid, exercise_number) in exercises:
        exercise_attempt_runs = get_time_run_number_pairings(participantid, exercise_number) #TODO: Remove this and replace with filtered program logs based on exercises and participant pairings. Can be done by creating filter functions for participant ids and exercises
        #Iterate through each run and add to the appropriate list based on whether it executed successfully. Array is a list of tuples is (run_time, participantid, edit_distance)
        for run in exercise_attempt_runs:
            if run[2]:
                successful_runs.append([run[1], names_to_offsets[participantid], (run[3] + 1) / 25])
            else:
                unsuccessful_runs.append([run[1], names_to_offsets[participantid], (run[3] + 1) / 25]) if run[3] < 300 else unsuccessful_runs.append([run[1], names_to_offsets[participantid], 1.5])

    ax.eventplot([[run[0]] for run in successful_runs], lineoffsets = [run[1] for run in successful_runs], linelengths=[run[2] for run in successful_runs], colors=successful_run_colour, label="Successful run")
    ax.eventplot([[run[0]] for run in unsuccessful_runs], lineoffsets = [run[1] for run in unsuccessful_runs], linelengths=[run[2] for run in unsuccessful_runs], colors=unsuccessful_run_colour, label="Unsuccessful run")
    handles, labels = ax.get_legend_handles_labels() 

    plt.legend([handles[0], handles[7]], [labels[0], labels[7]]) #Currently very hacky way of displaying two labels. Instead of index 7, get the first "Unsuccessful run" in the list.
    plt.yticks(line_offsets, names)
    plt.show()

def visualise_all_runs(*, filtered_ids: dict[str, list[str]], sort_by_exercise: bool, sort_by_student: bool, **kwargs):
    """  Creates a time series for each attempted exercise that conveys edit distance, repeated runs, and the success (outcome) of the run
            x: time since beginning of exercise (seconds), y: bars of each attempted exercise

    Args:k
        sort_by_exercise (bool): _description_
        sort_by_student (bool): _description_
    """
    #Set up plot
    fig, ax = plt.subplots()
    ax.set_xlabel("Time (seconds)")
    #ax.set_ylabel("Students' exercise attempts")
    #ax.set_title("A plot of every run on the debugging exercises. Each row represents a single exercise attempt, sorted by exercise number")
    offset_factor = -20 #Variables for managing spacing between each exercise
    offsets = [i * offset_factor for i in range(1,6)]

    #Get points to plot
    filtered_program_logs = get_filtered_program_logs(filtered_ids = filtered_ids, **kwargs)
    filtered_program_logs["time_on_task"] = filtered_program_logs["logs_snapshots"].apply(time_on_task)
    if sort_by_exercise:
        if sort_by_student:
            raise ValueError("sort_by_exercise and sort_by_student cannot both be true")
        filtered_program_logs = filtered_program_logs.sort_values(by=["exercise_number", "time_on_task"], ascending=False)
    elif sort_by_student:
        filtered_program_logs = filtered_program_logs.sort_values(by=["participantid", "time_on_task"])
    else:
        filtered_program_logs = filtered_program_logs.sort_values(by=["time_on_task"])
    points = get_points_data(filtered_program_logs)

    #Split points into successful and unsuccessful runs
    successful_points = [point for point in points if point.compiled]
    unsuccessful_points = [point for point in points if not point.compiled]

    ytick_offsets = []
    #Botch job of getting y ticks for exercise numbers in right place
    for i in range(1,6):
        temp = []
        for point in points:
            if point.exercise_number == i:
                temp.append(point.exerciseid + offsets[point.exercise_number - 1])
        ytick_offsets.append(median(temp) - offset_factor)

    ax.scatter([point.time_since_first_run for point in successful_points], [point.exerciseid + offsets[point.exercise_number - 1] for point in successful_points], s=1, color=successful_run_colour, label="Successful run")
    ax.scatter([point.time_since_first_run for point in unsuccessful_points], [point.exerciseid + offsets[point.exercise_number - 1] for point in unsuccessful_points], s=1, color=unsuccessful_run_colour, label="Unsuccessful run")

    plt.yticks(ytick_offsets,["Exercise 1","Exercise 2","Exercise 3", "Exercise 4", "Exercise 5"])
    plt.legend( markerscale=5)
    plt.show()
    #Required functions: get time of each run (x axis), success (outcome) of each run (tick/cross), whether run was repeated (colour), edit distance between previous run (size of tick). Return this as a 4-tuple array (or however big it is) 

def end_state_error_types(*, filtered_ids: dict[str, list[str]], **kwargs):
    """Creates a grouped bar chart to represent the end state of a set of exercise attempts. Grouped by exercise number, with different errors of each type.

    Args:
        dict[str, list[str]]: A dictionary containing a list of participantids (under the key 'participantid') who made an inconsequential change (same filtering logic used for stats functions).
    """
    exercise_numbers = ["Exercise 1","Exercise 2","Exercise 3","Exercise 4","Exercise 5"]
    fig, ax = plt.subplots(layout='constrained')
    width = 0.15  # the width of the bars
    multiplier = 0
    label_locations = np.arange(len(exercise_numbers))  # the label locations

    end_states = get_end_state_of_program(filtered_ids=filtered_ids, **kwargs)
    end_states.pop("Total attempts")
    
    #Logic taken from example on https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
    for error_type, counts in end_states.items():
        offset = width * multiplier
        rects = ax.bar(label_locations + offset, counts, width, label=error_type)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    
    ax.set_ylabel('n')
    ax.set_xticks(label_locations + width, exercise_numbers)
    ax.legend(loc='upper left', ncols=2)
    plt.show()

def create_case_study_visualisation():
    """ Function to create a particular figure to appear in the behaviour paper.
        In this case, we model the runs over time of three case studies: students 13, 28, and 33's attempts to exercise 4
    """
    model_time_over_runs_for_exercises([("7ed88c2f-5ae5-4d85-a0e1-ad2bf8593f56", 4),("7338a34d-6ba1-4e0f-a887-02d237d939b7", 4), ("2de71e2a-1d7c-4717-8135-018c5023e7a4", 4)], ["Manuela", "Declan", "Emile"] )

#visualise_all_runs(filtered_ids={}, sort_by_exercise=True, sort_by_student=False, **dataframes)
visualise_progress_over_time(filtered_ids={}, **dataframes)
#create_case_study_visualisation()