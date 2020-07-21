from sklearn.linear_model import LinearRegression
import datetime
import pandas


class Prediction(object):
    def __init__(self, data, days):
        # Creates variables
        self.data = data
        self.days = days
        self.new_dataframe = pandas.DataFrame()
        # Stores date in a separate variable as prediction won't handle strings
        self.date = self.data.index

    def machine_learning_prediction(self):
        # Iterate through columns
        for column in self.data:
            x = self.data.drop(column, 1)
            y = self.data[column]
            predictor = LinearRegression(n_jobs=-1)
            # Trains the predictor
            predictor.fit(x, y)
            # Predicts n days into future
            self.new_dataframe[column] = predictor.predict(x)[0:self.days]

    def date_generator(self):
        # Convert the first date to datetime object
        first_date = self.date[len(self.date)-1]
        future_date = []
        for day in range(1, self.days+1):
            future_date.append((first_date+datetime.timedelta(days=day)).strftime("%Y-%m-%d"))
        # Creates a column called date, and fills it with created dates
        self.new_dataframe["Date"] = pandas.DatetimeIndex(future_date)
        self.new_dataframe.set_index("Date", inplace=True)

    def manage_dataframe(self):
        # Joins dataframes together
        self.data = self.data.append(self.new_dataframe, sort=True)
        return self.data

