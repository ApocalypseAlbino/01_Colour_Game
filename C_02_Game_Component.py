import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows


def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded
    :return: rounded number
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# helper functions go here
def get_colours():
    """
    Retrieves colours from csv file
    :return: list of colours where each list item has the
    colour name, associated score and foreground colour for the text
    """

    file = open("00_colour_list_hex_v3(in).csv", "r")
    all_colours = list(csv.reader(file, delimiter=","))
    file.close()


def get_round_colours():
    """
    Choose four colours from larger list ensuring that the scores are all different
    :return: list of colours and score to beat (median of scores)
    """
    # Retrieve colours from csv file and put them in a list
    file = open("00_colour_list_hex_v3(in).csv", "r")
    all_colours = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove the first row
    all_colours.pop(0)

    round_colours = []
    colour_scores = []

    # loop until we have four colours with different scores...
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colours)

        # Get the score and check it's not a duplicate
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)
            colour_scores.append(potential_colour[1])

    # Find target score (median)
    int_scores = [int(x) for x in colour_scores]
    int_scores.sort()

    # Calculate the median
    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_colours, median  # Return both the colours and the median


class StartGame:
    """
    Initial Game interface which asks users how many rounds they want
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        intro_string = ("In each round you will be invited to choose a colour. Your goal is "
                        "to beat the target score and win the round (and keep your points)")

        # choose_string = "Oops - Please choose a whole number more than 0."
        choose_string = "How many rounds do you want to play"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # Create labels and add them to the reference list

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], wraplength=350, justify="left",
                               padx=20, pady=10)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be changed to an error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#fff", bg="#0057d8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve amount of rounds wanted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#fff")

        error = "Please choose a whole number more than 0"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute 0
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ieL hide rounds choice window)
                root.withdraw()
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#f4cccc")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the game
    """

    def __init__(self, how_many):

        # Integers / String Variables
        self.target_score = IntVar()

        # rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Colour lists and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {how_many}",
                                        font=("Arial", "16", "bold"))
        self.game_heading_label.grid(row=0, pady=10)

        self.score_to_beat_label = Label(self.game_frame, text="Score to beat: ",
                                         font=("Arial", "12"), bg="#fdf1ca")
        self.score_to_beat_label.grid(row=1, pady=10)

        self.instruction_label = Label(self.game_frame, text="Choose a colour below. Good luck.",
                                       font=("Arial", "12"), bg="#d8e4d6")
        self.instruction_label.grid(row=2, pady=10)

        # Colour buttons
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        # colour buttons (text | bg colour | command | row | column)
        colour_details_list = [
            ["Colour Name", "#f0f0f0", "", 0, 0],
            ["Colour Name", "#f0f0f0", "", 0, 1],
            ["Colour Name", "#f0f0f0", "", 1, 0],
            ["Colour Name", "#f0f0f0", "", 1, 1]
        ]

        # List to hold buttons once they have been made
        self.colour_ref_list = []

        for item in colour_details_list:
            self.make_button = Button(self.colour_frame,
                                      text=item[0], bg=item[1],
                                      fg="#000", font=("Arial", "12"),
                                      width=12, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            self.colour_ref_list.append(self.make_button)

        self.result_label = Label(self.game_frame, text="You chose, result",
                                  font=("Arial", "12"), bg="#d8e4d6")
        self.result_label.grid(row=4, pady=10)

        self.next_round_button = Button(self.game_frame, text="Next Round",
                                        font=("Arial", "16", "bold"),
                                        fg="#fff", bg="#0050cb",
                                        command="",
                                        width=18)
        self.next_round_button.grid(row=5, pady=10)

        # Other buttons
        self.button_frame = Frame(self.game_frame)
        self.button_frame.grid(row=6)

        # buttons (text | bg colour | command | row | column)
        button_details_list = [
            ["Hints", "#da7200", "", 0, 0],
            ["Stats", "#2b2a26", "", 0, 1],
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#fff", font=("Arial", "16", "bold"),
                                      width=8, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=6)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold"),
                                      fg="#fff", bg="#990000",
                                      command=self.close_play,
                                      width=18)
        self.end_game_button.grid(row=7, pady=10)

        # Once interface has been created, invoke new round function for first round
        self.new_round()

    def new_round(self):
        """
        Chooses four colours, works out median for score to beat. Configures buttons
        with chosen colours
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round colours and median score...
        self.round_colour_list, median = get_round_colours()

        self.target_score.set(median)

        # Update heading, and score to beat labels. "Hide" results label
        self.game_heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.score_to_beat_label.config(text=f"Target Score: {median}", font=("Arial", "14", "bold"))
        self.result_label.config(text=f"{'=' * 7}", bg="#f0f0f0")

        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of the last round)
        for count, item in enumerate(self.colour_ref_list):
            item.config(fg=self.round_colour_list[count][2],
                        bg=self.round_colour_list[count][0],
                        text=self.round_colour_list[count][0], state=NORMAL)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
