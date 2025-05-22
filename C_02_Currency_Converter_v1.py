from tkinter import *
from functools import partial
import conversion_rounding as cr  # Ensure this file exists


class Converter:
    """
    Currency conversion tool (NZD to GBP, NZD to USD, NZD to AUD)
    """

    def __init__(self):
        """
        Currency converter GUI
        """

        # Holds all converted values for exporting
        self.all_calculations_list = []

        # GUI Frame
        self.currency_frame = Frame(padx=10, pady=10)
        self.currency_frame.grid()

        # Heading (row 0)
        self.currency_heading = Label(self.currency_frame,
                                      text="Currency Converter",
                                      font=("Arial", "16", "bold"))
        self.currency_heading.grid(row=0)

        # Instructions (row 1)
        instructions = ("Please enter an amount in NZD below and then press "
                        "one of the buttons to convert it to AUD, USD or GBP.")
        self.currency_instructions = Label(self.currency_frame,
                                           text=instructions,
                                           wraplength=250, width=40,
                                           justify="left")
        self.currency_instructions.grid(row=1)

        # Entry Box (row 2)
        self.currency_entry = Entry(self.currency_frame, font=("Arial", "14"))
        self.currency_entry.grid(row=2, padx=10, pady=10)

        # Error message label (row 3)
        self.answer_error = Label(self.currency_frame, text="Please enter a number",
                                  fg="#084C99", font=("Arial", "14", "bold"))
        self.answer_error.grid(row=3)

        # Conversion, help and history/export buttons
        self.button_frame = Frame(self.currency_frame)
        self.button_frame.grid(row=4)

        # Button list: [text, bg colour, command, row, column]
        button_details_list = [
            ["To AUD", "#990099", partial(self.check_currency, 0), 0, 0],
            ["To USD", "#009900", partial(self.check_currency, 1), 0, 1],
            ["To GBP", "#003366", partial(self.check_currency, 2), 0, 2],
            ["Help / Info", "#CC6600", self.show_help, 1, 0],
            ["History / Export", "#004C99", self.show_history, 1, 1]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            btn = Button(self.button_frame,
                         text=item[0], bg=item[1],
                         fg="#FFFFFF", font=("Arial", "12", "bold"),
                         width=12, command=item[2])
            btn.grid(row=item[3], column=item[4], padx=5, pady=5)
            self.button_ref_list.append(btn)

        # Retrieve to_help button
        self.to_help_button = self.button_ref_list[3]

        # Retrieve 'history / export' button and disable it at the start
        self.to_history_button = self.button_ref_list[4]
        self.to_history_button.config(state=DISABLED)

    def check_currency(self, convert_mode):
        """
        Checks currency is valid and either invokes calculation
        function or shows a custom error
        """
        to_convert = self.currency_entry.get()

        # Reset visuals
        self.answer_error.config(fg="#004C99", font=("Arial", "13", "bold"))
        self.currency_entry.config(bg="#FFFFFF")

        # Error checking
        error = "Enter a valid number greater than or equal to 0"
        has_errors = False

        try:
            to_convert = float(to_convert)
            if to_convert >= 0:
                self.convert(convert_mode, to_convert)
            else:
                has_errors = True
        except ValueError:
            has_errors = True

        # Display error if needed
        if has_errors:
            self.answer_error.config(text=error, fg="#9C0000", font=("Arial", "10", "bold"))
            self.currency_entry.config(bg="#F4CCCC")
            self.currency_entry.delete(0, END)

    def convert(self, convert_mode, to_convert):
        """
        Performs the currency conversion based on the button clicked
        """
        if convert_mode == 0:
            answer = cr.to_AUD(to_convert)
            answer_statement = f"{to_convert} NZD is {answer} AUD"
        elif convert_mode == 1:
            answer = cr.to_USD(to_convert)
            answer_statement = f"{to_convert} NZD is {answer} USD"
        else:
            answer = cr.to_GBP(to_convert)
            answer_statement = f"{to_convert} NZD is {answer} GBP"

        # Enable history button + update output label
        self.to_history_button.config(state=NORMAL)
        self.answer_error.config(text=answer_statement)
        self.all_calculations_list.append(answer_statement)

    def show_help(self):
        """
        Dummy Help / Info popup
        """
        print("Help button clicked")

    def show_history(self):
        """
        Dummy History / Export popup
        """
        print("History button clicked")


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()
