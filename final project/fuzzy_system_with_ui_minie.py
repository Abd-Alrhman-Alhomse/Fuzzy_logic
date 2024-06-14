from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import tkinter as tk
import numpy as np

# Define Antecedents
team_performance = ctrl.Antecedent(np.arange(0, 101, 1), 'team_performance')
players_statistics = ctrl.Antecedent(np.arange(0, 101, 1), 'players_statistics')
weather_conditions = ctrl.Antecedent(np.arange(0, 101, 1), 'weather_conditions')

# Define Consequents
match_outcome_condition = ctrl.Consequent(np.arange(0, 101, 1), 'match_outcome')

# Define the membership functions for team_performance
team_performance['poor'] = fuzz.gaussmf(team_performance.universe, 0, 15)
team_performance['average'] = fuzz.gaussmf(team_performance.universe, 50, 15)
team_performance['excellent'] = fuzz.gaussmf(team_performance.universe, 100, 15)

# Define the membership functions for speech
players_statistics['low'] = fuzz.gaussmf(players_statistics.universe, 0, 15)
players_statistics['medium'] = fuzz.gaussmf(players_statistics.universe, 50, 15)
players_statistics['high'] = fuzz.gaussmf(players_statistics.universe, 100, 15)

# Define the membership functions for medical history
weather_conditions['bad'] = fuzz.gaussmf(weather_conditions.universe, 0, 15)
weather_conditions['Moderate'] = fuzz.gaussmf(weather_conditions.universe, 50, 15)
weather_conditions['good'] = fuzz.gaussmf(
    weather_conditions.universe, 100, 15)

# Define the membership functions for the output variable
match_outcome_condition['Loss'] = fuzz.gaussmf(
match_outcome_condition.universe, 0, 15)
match_outcome_condition['Draw'] = fuzz.gaussmf(
match_outcome_condition.universe, 50, 15)
match_outcome_condition['Win'] = fuzz.gaussmf(
match_outcome_condition.universe, 100, 15)

# Define the rules
rule1 = ctrl.Rule(team_performance["poor"] & players_statistics["low"] &
                  weather_conditions["bad"], match_outcome_condition["Loss"])
rule2 = ctrl.Rule(
    (team_performance["excellent"] | players_statistics["high"]), match_outcome_condition["Win"])
rule3 = ctrl.Rule(weather_conditions["good"] & (
    team_performance["average"] | players_statistics["medium"]), match_outcome_condition["Win"])
rule4 = ctrl.Rule(team_performance["average"] & players_statistics["medium"]
                  & weather_conditions["Moderate"], match_outcome_condition["Draw"])
rule5 = ctrl.Rule(team_performance["poor"] & (
    players_statistics["low"] | weather_conditions["bad"]), match_outcome_condition["Loss"])

# Create the control system
match_outcome_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
match_outcome_d = ctrl.ControlSystemSimulation(match_outcome_ctrl)

# Define Membership Function Drawing


def show_membership_functions():
    # Create a new figure and plot the membership functions
    fig = plt.figure()
    match_outcome_condition.view(sim=match_outcome_d)
    plt.title('Membership Functions')

    # Create a canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add a toolbar to the canvas
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Define the UI
def d_match_condation():
    # Get the input values from the UI
    team_performance = float(team_performance_input.get())
    players_statistics = float(players_statistics_input.get())
    weather_conditions = float(weather_conditions_input.get())

    # Pass the input values to the control system
    match_outcome_d.input['team_performance'] = team_performance
    match_outcome_d.input['players_statistics'] = players_statistics
    match_outcome_d.input['weather_conditions'] = weather_conditions

    # Compute the output value
    match_outcome_d.compute()

    # Get the output value from the control system
    predict = match_outcome_d.output['match_outcome']

    # Display the predict number
    predict_label_number.config(
        text='predict: ' + str(round(predict, 2)))

    # Display the predict category
    if predict <= 40:
        predict_label_category.config(text='condation: Loss')
    elif 40 <= predict <= 70:
       predict_label_category.config(text='condation: Draw')
    else:
        predict_label_category.config(text='condation: Win')

    # Show the membership functions in a new window
    show_membership_functions()


# Create the UI
root = tk.Tk()
root.title('predicting the outcome of a cricket match')

team_performance_label = tk.Label(root, text='team_performance:')
team_performance_label.grid(row=0, column=0)
team_performance_input = tk.Entry(root)
team_performance_input.grid(row=0, column=1)

players_statistics_label = tk.Label(root, text='players_statistics:')
players_statistics_label.grid(row=1, column=0)
players_statistics_input = tk.Entry(root)
players_statistics_input.grid(row=1, column=1)

weather_conditions_label = tk.Label(root, text='weather_conditions:')
weather_conditions_label.grid(row=2, column=0)
weather_conditions_input = tk.Entry(root)
weather_conditions_input.grid(row=2, column=1)

predict_button = tk.Button(root, text='predict',
                            command=d_match_condation)
predict_button.grid(row=3, column=0)

predict_label_number = tk.Label(root, text='predict Number: ')
predict_label_number.grid(row=3, column=1)

predict_label_category = tk.Label(root, text='predict Category: ')
predict_label_category.grid(row=4, column=1)

root.mainloop()
