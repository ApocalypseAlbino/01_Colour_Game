import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows


def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded.
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
    highest = int_scores[-1]

    return round_colours, median, highest


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
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")
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

        self.rounds_won = IntVar()

        # Colour lists and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_high_score_list = []

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

        # List to hold buttons once they have been made
        self.colour_ref_list = []

        # Create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.color_button = Button(self.colour_frame, font="Arial 12",
                                       text="Colour Name", width=15,
                                       command=partial(self.round_results, item))
            self.color_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)
            self.colour_ref_list.append(self.color_button)

        self.result_label = Label(self.game_frame, text="You chose, result",
                                  font=("Arial", "12"), bg="#d8e4d6")
        self.result_label.grid(row=4, pady=10)

        self.next_round_button = Button(self.game_frame, text="Next Round",
                                        font=("Arial", "16", "bold"),
                                        fg="#fff", bg="#0050cb",
                                        command=self.new_round,
                                        width=18)
        self.next_round_button.grid(row=5, pady=10)

        # Other buttons
        self.button_frame = Frame(self.game_frame)
        self.button_frame.grid(row=6)

        # buttons (text | bg colour | command | row | column)
        button_details_list = [
            ["Hints", "#da7200", self.to_hints, 0, 0],
            ["Stats", "#2b2a26", self.to_stats, 0, 1],
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []
        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#fff", font=("Arial", "16", "bold"),
                                      width=8, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=6)

            self.button_ref_list.append(self.make_button)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold"),
                                      fg="#fff", bg="#990000",
                                      command=self.close_play,
                                      width=18)
        self.end_game_button.grid(row=7, pady=10)

        self.hints_button = self.button_ref_list[0]
        self.stats_button = self.button_ref_list[1]

        self.stats_button.config(state=DISABLED)

        # Once interface has been created, invoke new round function for first round
        self.new_round()

    def to_hints(self):
        """
        Displays hints for playing game
        """
        DisplayHelp(self)

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
        self.round_colour_list, median, highest = get_round_colours()

        self.target_score.set(median)

        # add high score to list for stats...
        self.all_high_score_list.append(highest)

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

        self.next_round_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0-3), retrieves
        score and then compares it within median, updates results
        and adds itself to the stats list
        """

        # Get user score and colour based on button press
        score = int(self.round_colour_list[user_choice][1])

        # alternate way to get button name. Good for if buttons have been scrambled
        colour_name = self.colour_ref_list[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        target = self.target_score.get()

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#82b366"
            self.all_scores_list.append(score)

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)

        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target"
            result_bg = "#f8cecc"
            self.all_scores_list.append(0)

        self.result_label.config(text=result_text, bg=result_bg)

        # enable stats and next buttons, disable colour buttons
        self.next_round_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_round_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.colour_ref_list:
            item.config(state=DISABLED)

    def to_stats(self):
        """
        Displays everything we need to display the game / round statistics
        """

        # IMPORTANT: retrieve number of rounds won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list, self.all_high_score_list]

        Stats(self, stats_bundle)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


class DisplayHelp:

    def __init__(self, partner):

        # set up dialogue box and background color
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable button
        partner.hints_button.config(state=DISABLED)

        # If users press 'X' instead of dismiss, unblocks help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Hints",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "The score for each colour relates to it's hexadecimal code." \
                    "\n\n" \
                    "Remember, the hex code for white is #FFFFFF - which is the best possible score." \
                    "\n\n" \
                    "The hex code for black is #000000 which is the worst possible score." \
                    "\n\n" \
                    "The first colour in the code is red, so if you had to choose between red (#FF0000), " \
                    "green (#00FF00) and blue (#0000FF), then red would be the best choice." \
                    "\n\n" \
                    "Good Luck!"

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#cc6600",
                                     fg="#fff",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List of everything to put background colour on
        recolour_list = (self.help_frame, self.help_heading_label,
                         self.help_text_label)

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        partner.hints_button.config(state=NORMAL)  # Re-enable the button
        self.help_box.destroy()


class Stats:

    def __init__(self, partner, all_stats_info):

        # Extract information from master list...
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]
        high_scores = all_stats_info[2]

        # Sort user scores to find high score
        user_scores.sort()

        self.stat_box = Toplevel()

        # disable button
        partner.stats_button.config(state=DISABLED)

        # If users press 'X' instead of dismiss, unblocks stat button
        self.stat_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_stat, partner))

        self.stat_frame = Frame(self.stat_box, width=300,
                                height=200)
        self.stat_frame.grid()

        # Math to populate Stats dialogue...
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # Strings for Stats labels

        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum Possible Score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"

        # Custom comment text and formatting
        if total_score == max_possible:
            comment_string = "Amazing! You got the highest possible score!"
            comment_colour = "#d5e8d4"

        elif total_score == 0:
            comment_string = "Oops - You've lost every round! Maybe check the hints 😉"
            comment_colour = "#f8cecc"
            best_score_string = f"Best Score: n/a"
        else:
            comment_string = ""
            comment_colour = "#f0f0f0"

        average_score_string = f"Average Score: {average_score:.0f}\n"

        heading_font = "Arial 16 bold"
        normal_font = "Arial 14"
        comment_font = "Arial 13"

        # Label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stat_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stat_frame,
                                     font="Arial 16 bold", text="Dismiss",
                                     bg="#333333", fg="#ffffff", width=20,
                                     command=partial(self.close_stat, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    def close_stat(self, partner):
        partner.stats_button.config(state=NORMAL)  # Re-enable the button
        self.stat_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
