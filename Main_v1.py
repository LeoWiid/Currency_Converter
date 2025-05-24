from tkinter import *
from functools import partial
import conversion_rounding as cr  # make sure this file exists with to_AUD, to_USD, and to_GBP functions
from datetime import date


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
                                      text="SchmeckleTwister: Currency for Clowns  ",
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

        # Conversion, help and history / expert buttons
        self.button_frame = Frame(self.currency_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To AUD", "#990099", partial(self.check_currency, 0), 0, 0],
            ["To USD", "#009900", partial(self.check_currency, 1), 0, 1],
            ["To GBP", "#003366", partial(self.check_currency, 2), 0, 2],
            ["Help / Info", "#CC6600", self.to_help, 1, 0],
            ["History / Export", "#004C99", self.to_history, 1, 2]
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

        # retrieve 'history / export' button and disable it at the start
        self.to_history_button = self.button_ref_list[4]
        self.to_history_button.config(state=DISABLED)

    def check_currency(self, convert_mode):
        """
        Checks currency is valid, limits input to 8 digits,
        and either invokes calculation function or shows a custom error.
        """
        to_convert = self.currency_entry.get()

        # Reset error message & entry box colour
        self.answer_error.config(fg="#004C99", font=("Arial", "13", "bold"))
        self.currency_entry.config(bg="#FFFFFF")

        # Error checking
        error = "Enter a valid amount greater than 10 cents and no larger than 8 digits"
        has_errors = False

        try:
            # Check if input is a number
            to_convert_float = float(to_convert)

            # Remove decimal point and count digits only
            digit_count = len(to_convert.replace(".", "").replace("-", ""))

            if to_convert_float >= 0.1 and digit_count <= 8:
                self.convert_currency(convert_mode, to_convert_float)
            else:
                has_errors = True
        except ValueError:
            has_errors = True

        # Display error if needed
        if has_errors:
            self.answer_error.config(text=error, fg="#9C0000", font=("Arial", "10", "bold"))
            self.currency_entry.config(bg="#F4CCCC")
            self.currency_entry.delete(0, END)

    def convert_currency(self, convert_mode, to_convert):
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

    def to_help(self):
        DisplayHelp(self)

    def to_history(self):
        HistoryExport(self, self.all_calculations_list)


class DisplayHelp:
    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # Disable help button
        partner.to_help_button.config(state=DISABLED)

        # Re-enable help button on close
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"),
                                        bg=background)
        self.help_heading_label.grid(row=0)

        help_text = ("To use the program, enter an amount in NZD, then click "
                     "'To AUD', 'To USD', or 'To GBP'.\n\n"
                     "You can view and export your conversion history using the "
                     "'History / Export' button.")
        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left", bg=background)
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


class HistoryExport:
    def __init__(self, partner, calculations):
        self.history_box = Toplevel()
        partner.to_history_button.config(state=DISABLED)
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box)
        self.history_frame.grid()

        calc_amount = "all your" if len(calculations) <= 5 \
            else f"your recent calculations - showing 5 / {len(calculations)}"
        recent_intro_txt = f"Below are {calc_amount} calculations."

        newest_first_list = list(reversed(calculations))
        newest_first_string = "\n".join(newest_first_list[:5])

        export_instruction_txt = ("Please push <Export> to save your calculations in a file. "
                                  "If the filename already exists, it will be replaced.")

        label_details = [
            ["History / Export", ("Arial", "16", "bold"), None],
            [recent_intro_txt, ("Arial", "11"), None],
            [newest_first_string, ("Arial", "14"), "#D5E8D4"],
            [export_instruction_txt, ("Arial", "11"), None]
        ]

        self.label_refs = []
        for i, (text, font_style, bg) in enumerate(label_details):
            lbl = Label(self.history_box, text=text, font=font_style,
                        bg=bg, wraplength=300, justify="left", pady=10, padx=20)
            lbl.grid(row=i)
            self.label_refs.append(lbl)

        self.export_filename_label = self.label_refs[3]

        self.history_button_frame = Frame(self.history_box)
        self.history_button_frame.grid(row=4)

        Button(self.history_button_frame, font=("Arial", "12", "bold"),
               text="Export", bg="#004C99", fg="#FFFFFF", width=12,
               command=lambda: self.export_data(calculations)).grid(row=0, column=0, padx=10, pady=10)

        Button(self.history_button_frame, font=("Arial", "12", "bold"),
               text="Close", bg="#666666", fg="#FFFFFF", width=12,
               command=partial(self.close_history, partner)).grid(row=0, column=1, padx=10, pady=10)

    def export_data(self, calculations):
        today = date.today()
        file_name = f"currency_{today.strftime('%Y_%m_%d')}.txt"

        with open(file_name, "w") as f:
            f.write("***** Currency Calculations ******\n")
            f.write(f"Generated: {today.strftime('%d/%m/%Y')}\n\n")
            f.write("Here is your calculation history (oldest to newest)...\n")
            for item in calculations:
                f.write(item + "\n")

        self.export_filename_label.config(bg="#009900",
                                          text=f"Export Successful! File: {file_name}",
                                          font=("Arial", "12", "bold"))

    def close_history(self, partner):
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()
