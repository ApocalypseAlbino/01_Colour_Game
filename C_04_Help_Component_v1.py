import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows


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

        # Create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#fff", bg="#0057d8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve amount of rounds wanted
        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes Game GUI and takes across number of rounds to be played
        """
        Play(num_rounds)
        # Hide root window (ie: hide round choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Colour Quest", font="Arial 16 bold",
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.hints_button = Button(self.game_frame, font="Arial 14 bold",
                                   text="Hints", width=15, fg="#fff",
                                   bg="#ff8000", padx=10, pady=10, command=self.to_hints)
        self.hints_button.grid(row=1)

    def to_hints(self):
        """
        Displays hints for playing game
        """
        DisplayHelp(self)


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


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
