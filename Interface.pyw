import tkinter as tk
import pyautogui
import string
import datetime
from Import import Import
from Graph import Graph
from Prediction import Prediction


class Interface(object):
    # Main function, executes all commands configuring the window
    def __init__(self):
        self.master = tk.Tk()
        self.green = "#32CD32"
        self.red = "#B22222"
        self.get_resolution()
        self.configure_window()
        self.place_grid()

        self.stock_name = tk.StringVar()
        self.stock_input()

        self.date_input()

        self.start_day = tk.StringVar()
        self.start_day_input()

        self.start_month = tk.StringVar()
        self.start_month_input()

        self.start_year = tk.StringVar()
        self.start_year_input()

        self.end_day = tk.StringVar()
        self.end_day_input()

        self.end_month = tk.StringVar()
        self.end_month_input()

        self.end_year = tk.StringVar()
        self.end_year_input()

        self.open = tk.IntVar()
        self.high = tk.IntVar()
        self.close = tk.IntVar()
        self.low = tk.IntVar()
        self.data_type_input()

        self.prediction_type = tk.IntVar()
        self.prediction_type_input()

        self.graph_type = tk.StringVar()
        self.choices = {"Linear", "Bar", "Area", "Scatter", "Candle"}
        self.graph_type_input()

        # Run and Reset buttons
        self.reset_input()
        self.run_input()

        self.master.mainloop()

    # Gets resolution and applies it to the window
    def get_resolution(self):
        scale = 0.5
        # Gets size of the screen
        resolution = pyautogui.size()
        resolution = [round(dimension * scale) for dimension in resolution]
        # Converts resolution into the format accepted by the program
        resolution = "%sx%s" % (resolution[0], resolution[1])
        self.master.geometry(resolution)
        # Doesn't allow user to rescale the window
        self.master.resizable(width=False, height=False)

    # Responsible for the window configuration (Colour, style etc.)
    def configure_window(self):
        self.master.title("The Trading Oracle")
        self.master.iconbitmap("icon.ico")
        self.master.configure(background="#A9A9A9")

    # Creates 101x101 grid for allocation of all elements
    def place_grid(self):
        for i in range(0, 101):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    # Places the widgets for the stock input
    def stock_input(self):
        # Informative label
        stock_label = tk.Label(self.master, text="Stock Name:", width=10)
        stock_label.grid(row=4, column=50)
        # Validates the variable
        self.stock_name.trace('w', self.stock_validation)
        # Form input for stock name
        stock_entry = tk.Entry(self.master, textvariable=self.stock_name)
        # Places the entry widget on the grid
        stock_entry.config(width=10)
        stock_entry.grid(row=5, column=50)
        # Button to check its existence
        stock_button = tk.Button(self.master, text="Check", command=self.check_stock)
        stock_button.grid(row=5, column=51)

    # Validates whether the stock only uses 5 Capital letters
    def stock_validation(self, *args):
        # Gets the variable from the text box
        new_input = self.stock_name.get()
        # Checks whether it is longer than 0
        if len(new_input) > 0:
            # Checks whether it only contains letters or is longer than 5 characters
            if new_input[-1] not in string.ascii_letters or len(new_input) > 5:
                # if not, removes the last symbol inserted
                new_input = new_input[:-1]
        # Capitalises all letters
        new_input = new_input.upper()
        # Updates the text box
        self.stock_name.set(new_input)

    def check_stock(self):
        import_module = Import(self.stock_name.get(), "", "")
        if import_module.stock_check():
            self.right_stock()
            return True
        else:
            self.wrong_stock()
            return False

    def right_stock(self):
        stock_label = tk.Label(self.master, text="Stock Name:", width=10)
        stock_label.configure(bg=self.green)
        stock_label.grid(row=4, column=50)

        stock_button = tk.Button(self.master, text="Check", command=self.check_stock)
        stock_button.configure(bg=self.green)
        stock_button.grid(row=5, column=51)

    def wrong_stock(self):
        stock_label = tk.Label(self.master, text="Stock Name:", width=10)
        stock_label.configure(bg=self.red)
        stock_label.grid(row=4, column=50)

        stock_button = tk.Button(self.master, text="Check", command=self.check_stock)
        stock_button.configure(bg=self.red)
        stock_button.grid(row=5, column=51)

    def date_input(self):
        # Informative Label
        date_label = tk.Label(self.master, text="Starting Date:", width=10)
        date_label.grid(row=8, column=44)
        date_label = tk.Label(self.master, text="Ending Date:", width=10)
        date_label.grid(row=9, column=44)
        # Places a dash next to the date, to separate entry widgets
        dash_label = tk.Label(self.master, text="-")
        dash_label.grid(row=8, column=46)
        dash_label = tk.Label(self.master, text="-")
        dash_label.grid(row=8, column=48)
        dash_label = tk.Label(self.master, text="-")
        dash_label.grid(row=9, column=46)
        dash_label = tk.Label(self.master, text="-")
        dash_label.grid(row=9, column=48)

    def check_date_and_prediction(self):
        # Sets us try-except block
        try:
            # Tries to create a datetime object, function would throw out a Value error is the date is not viable
            start = datetime.datetime(int(self.start_year.get()), int(self.start_month.get()),
                                      int(self.start_day.get()))
            end = datetime.datetime(int(self.end_year.get()), int(self.end_month.get()), int(self.end_day.get()))
            # Checks whether the starting date happened earlier than the end date
            if end < start:
                pass
            # Checks whether end date happened in the future if no prediction was set
            elif end > datetime.datetime.today() and self.prediction_type.get() == 1:
                pass
            # Checks whether start date is in the future if MI or SA prediction was set
            elif start > datetime.datetime.today() and self.prediction_type.get() in (2, 3):
                pass
            # If neither of conditions was executed, the date and prediction are correct
            else:
                self.right_date()
                self.right_prediction_type()
                return True
            # If any of conditions is executed, the date or prediction is incorrect
            self.wrong_date()
            self.wrong_prediction_type()
            return False
        # If exception is a ValueError, return information about incorrect date
        except ValueError:
            self.wrong_date()
            self.wrong_prediction_type()

    def right_date(self):
        date_label = tk.Label(self.master, text="Starting Date:", width=10)
        date_label.config(bg=self.green)
        date_label.grid(row=8, column=44)

        date_label = tk.Label(self.master, text="Ending Date:", width=10)
        date_label.config(bg=self.green)
        date_label.grid(row=9, column=44)

    def wrong_date(self):
        date_label = tk.Label(self.master, text="Starting Date:", width=10)
        date_label.config(bg=self.red)
        date_label.grid(row=8, column=44)

        date_label = tk.Label(self.master, text="Ending Date:", width=10)
        date_label.config(bg=self.red)
        date_label.grid(row=9, column=44)

    def start_day_input(self):
        # Validates the variable
        self.start_day.trace('w', self.start_day_validation)
        # Form input for stock name
        start_day_entry = tk.Entry(self.master, textvariable=self.start_day)
        # Places the entry widget on the grid
        start_day_entry.config(width=2)
        start_day_entry.grid(row=8, column=45)

    def start_day_validation(self, *args):
        new_input = self.start_day.get()
        if len(new_input) > 0:
            if new_input[-1] not in string.digits or len(new_input) > 2:
                new_input = new_input[:-1]
        if len(new_input) > 0:
            if int(new_input) > 31:
                new_input = "31"
        self.start_day.set(new_input)

    def start_month_input(self):
        # Validates the variable
        self.start_month.trace('w', self.start_month_validation)
        # Form input for stock name
        start_month_entry = tk.Entry(self.master, textvariable=self.start_month)
        # Places the entry widget on the grid
        start_month_entry.config(width=2)
        start_month_entry.grid(row=8, column=47)

    def start_month_validation(self, *args):
        new_input = self.start_month.get()
        if len(new_input) > 0:
            if new_input[-1] not in string.digits or len(new_input) > 2:
                new_input = new_input[:-1]
        if len(new_input) > 0:
            if int(new_input) > 12:
                new_input = "12"
        self.start_month.set(new_input)

    def start_year_input(self):
        # Validates the variable
        self.start_year.trace('w', self.start_year_validation)
        # Form input for stock name
        start_year_entry = tk.Entry(self.master, textvariable=self.start_year)
        # Places the entry widget on the grid
        start_year_entry.config(width=4)
        start_year_entry.grid(row=8, column=49)

    def start_year_validation(self, *args):
        current_year = datetime.datetime.now().year
        new_input = self.start_year.get()
        if len(new_input) > 0:
            if new_input[-1] not in string.digits or len(new_input) > 4:
                new_input = new_input[:-1]
            if len(new_input) == 4:
                if int(new_input) < 2000:
                    new_input = "2000"
                if int(new_input) > current_year:
                    new_input = current_year
        self.start_year.set(new_input)

    def end_day_input(self):
        # Validates the variable
        self.end_day.trace('w', self.end_day_validation)
        # Form input for stock name
        end_day_entry = tk.Entry(self.master, textvariable=self.end_day)
        # Places the entry widget on the grid
        end_day_entry.config(width=2)
        end_day_entry.grid(row=9, column=45)

    def end_day_validation(self, *args):
        new_input = self.end_day.get()
        if len(new_input) > 0:
            if new_input[-1] not in string.digits or len(new_input) > 2:
                new_input = new_input[:-1]
        if len(new_input) > 0:
            if int(new_input) > 31:
                new_input = "31"
        self.end_day.set(new_input)

    def end_month_input(self):
        # Validates the variable
        self.end_month.trace('w', self.end_month_validation)
        # Form input for stock name
        end_month_entry = tk.Entry(self.master, textvariable=self.end_month)
        # Places the entry widget on the grid
        end_month_entry.config(width=2)
        end_month_entry.grid(row=9, column=47)

    def end_month_validation(self, *args):
        new_input = self.end_month.get()
        if len(new_input) > 0:
            if new_input[-1] not in string.digits or len(new_input) > 2:
                new_input = new_input[:-1]
        if len(new_input) > 0:
            if int(new_input) > 12:
                new_input = "12"
        self.end_month.set(new_input)

    def end_year_input(self):
        # Validates the variable
        self.end_year.trace('w', self.end_year_validation)
        # Form input for stock name
        end_year_entry = tk.Entry(self.master, textvariable=self.end_year)
        # Places the entry widget on the grid
        end_year_entry.config(width=4)
        end_year_entry.grid(row=9, column=49)

    def end_year_validation(self, *args):
        new_input = self.end_year.get()
        if len(new_input) > 0:
            if new_input[-1] not in string.digits or len(new_input) > 4:
                new_input = new_input[:-1]
            if len(new_input) == 4:
                if int(new_input) < 2000:
                    new_input = "2000"
        self.end_year.set(new_input)

    def data_type_input(self):
        # Informative Label
        data_types_label = tk.Label(self.master, text="Data types:")
        data_types_label.grid(row=7, column=52, columnspan=2)
        # Open Data type
        open_box = tk.Checkbutton(self.master, text="open", variable=self.open, width=5)
        open_box.grid(row=8, column=52)
        # High Data type
        high_box = tk.Checkbutton(self.master, text="high", variable=self.high, width=5)
        high_box.grid(row=9, column=52)
        # Close Data type
        close_box = tk.Checkbutton(self.master, text="close", variable=self.close, width=5)
        close_box.grid(row=8, column=53)
        # Low Data type
        low_box = tk.Checkbutton(self.master, text="low", variable=self.low, width=5)
        low_box.grid(row=9, column=53)

    def check_data_type_and_graph(self):
        # Assigns user input to variables
        open = self.open.get()
        close = self.close.get()
        high = self.high.get()
        low = self.low.get()
        # Checks whether at least one data type was selected
        if low+close+high+open == 0:
            pass
        # Checks whether all datatypes were selected for a candle graph
        elif low+close+high+open != 4 and self.graph_type.get() == "Candle":
            pass
        # Checks whether only one data type selected for linear or scatter graph
        elif open+close+high+low != 1 and self.prediction_type.get() != 2 and \
                (self.graph_type.get() == "Linear"
                 or self.graph_type.get() == "Scatter"):
            pass
        # Checks whether low and high selected when dealing with bar or area graphs
        elif not (low and high and not open and not close) and (
                self.graph_type.get() == "Bar" or self.graph_type.get() == "Area"):
            pass
        else:
            self.right_data_type()
            self.right_graph_type()
            return True
        self.wrong_data_type()
        self.wrong_graph_type()
        return False

    def right_data_type(self):
        data_types_label = tk.Label(self.master, text="Data types:")
        data_types_label.configure(bg=self.green)
        data_types_label.grid(row=7, column=52, columnspan=2)

    def wrong_data_type(self):
        data_types_label = tk.Label(self.master, text="Data types:")
        data_types_label.configure(bg=self.red)
        data_types_label.grid(row=7, column=52, columnspan=2)

    def prediction_type_input(self):
        # Informative label
        prediction_type_label = tk.Label(self.master, text="Prediction type:")
        prediction_type_label.grid(row=10, column=52, columnspan=2)
        # Radio buttons
        # No Prediction
        # Label
        no_prediction_label = tk.Label(self.master, text="No Prediction:", width=11)
        no_prediction_label.grid(row=11, column=52, columnspan=2, sticky="W")
        # Creation of radio button
        no_prediction_button = tk.Radiobutton(self.master, variable=self.prediction_type, value=1)
        no_prediction_button.grid(row=11, column=53)
        # Machine Learning
        # Label
        machine_learning_label = tk.Label(self.master, text="Expert System:", width=11)
        machine_learning_label.grid(row=12, column=52, columnspan=2, sticky="W")
        # Creation of radio button
        machine_learning_button = tk.Radiobutton(self.master, variable=self.prediction_type, value=2)
        machine_learning_button.grid(row=12, column=53)
        self.prediction_type.set(1)

    def right_prediction_type(self):
        prediction_type_label = tk.Label(self.master, text="Prediction type:")
        prediction_type_label.configure(bg=self.green)
        prediction_type_label.grid(row=10, column=52, columnspan=2)

    def wrong_prediction_type(self):
        prediction_type_label = tk.Label(self.master, text="Prediction type:")
        prediction_type_label.configure(bg=self.red)
        prediction_type_label.grid(row=10, column=52, columnspan=2)

    def graph_type_input(self):
        # Informative label
        graph_type_label = tk.Label(self.master, text="Graph type:", width=10)
        graph_type_label.grid(row=10, column=44)
        # Drop-down menu
        graph_type_menu = tk.OptionMenu(self.master, self.graph_type, *self.choices)
        graph_type_menu.grid(row=10, column=45, columnspan=5)
        # Default choice
        self.graph_type.set("Candle")

    def right_graph_type(self):
        graph_type_label = tk.Label(self.master, text="Graph type:", width=10)
        graph_type_label.configure(bg=self.green)
        graph_type_label.grid(row=10, column=44)

    def wrong_graph_type(self):
        graph_type_label = tk.Label(self.master, text="Graph type:", width=10)
        graph_type_label.configure(bg=self.red)
        graph_type_label.grid(row=10, column=44)

    def reset_input(self):
        # Reset Button
        reset_button = tk.Button(self.master, text="Reset", command=self.reset_command)
        reset_button.grid(row=50, column=50)

    def reset_command(self):
        # Resets everything to default
        # Resets entry box for stock
        self.stock_name.set("ADYEN")
        # Resets start date
        self.start_day.set("12")
        self.start_month.set("12")
        self.start_year.set("2019")
        # Resets end date
        self.end_day.set("12")
        self.end_month.set("06")
        self.end_year.set("2020")
        # Resets data types
        self.open.set(1)
        self.close.set(1)
        self.high.set(1)
        self.low.set(1)
        # Resets prediction type
        self.prediction_type.set(2)
        # Resets graph type
        self.graph_type.set("Candle")
        # Resets colours
        self.stock_input()
        self.date_input()
        self.data_type_input()
        self.prediction_type_input()
        self.graph_type_input()
        self.run_input()

    def run_input(self):
        # Run Button
        run_button = tk.Button(self.master, text="Run", command=self.run_command)
        run_button.grid(row=50, column=44)

    def run_command(self):
        valid = True
        # Validation routine, evaluates every condition to make sure that user knows wrong elements
        # Checks stock, returns True if correct
        if not self.check_stock():
            valid = False
        # Checks date and prediction, returns True if correct
        if not self.check_date_and_prediction():
            valid = False
        # Checks data type and graph, returns True if correct
        if not self.check_data_type_and_graph():
            valid = False
        # Running the program
        if valid:
            self.right_run()
            start_date = self.start_year.get() + "-" + self.start_month.get() + "-" + self.start_day.get()
            end_date = self.end_year.get() + "-" + self.end_month.get() + "-" + self.end_day.get()
            # Initiates import module
            stock_name = self.stock_name.get()
            if self.prediction_type.get() == 1:
                import_module = Import(stock_name, start_date, end_date)
            else:
                import_module = Import(stock_name, start_date, datetime.datetime.today().strftime('%Y-%m-%d'))
            # Imports data
            data = import_module.import_data()
            # Drops columns which are not required
            if not self.open.get():
                data.drop(["Open"], axis=1, inplace=True)
            if not self.high.get():
                data.drop(["High"], axis=1, inplace=True)
            if not self.low.get():
                data.drop(["Low"], axis=1, inplace=True)
            if not self.close.get():
                data.drop(["Close"], axis=1, inplace=True)
            # Predicts future prices
            if self.prediction_type.get() != 1:
                # Calculated a number of days between current date and future
                days = datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.today()
                if days.days > 30:
                     days = 31
                else:
                    days = days.days + 1

                prediction_module = Prediction(data, days)
                prediction_module.machine_learning_prediction()

                prediction_module.date_generator()
                data = prediction_module.manage_dataframe()
            # Initiates graph module
            graph_module = Graph(stock_name, data)
            # Convert dates to numerical values
            # Stores graph type in a variable
            graph = self.graph_type.get()
            # Initiates appropriate graph
            if graph == "Candle":
                graph_module.candle_graph()
            elif graph == "Scatter":
                graph_module.scatter_graph()
            elif graph == "Linear":
                graph_module.linear_graph()
            elif graph == "Area":
                graph_module.area_graph()
            elif graph == "Bar":
                graph_module.bar_graph()
            # Starts the graph
            if graph != "Candle":
                graph_module.start_graph()
        else:
            self.wrong_run()

    def right_run(self):
        run_button = tk.Button(self.master, text="Run", command=self.run_command)
        run_button.config(bg=self.green)
        run_button.grid(row=50, column=44)

    def wrong_run(self):
        run_button = tk.Button(self.master, text="Run", command=self.run_command)
        run_button.config(bg=self.red)
        run_button.grid(row=50, column=44)


app = Interface()
