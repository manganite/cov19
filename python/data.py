import pandas as pd


class Data():

    def get_data(self):
        self.dtf_cases = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", sep=",")
        self.countrylist = ["World"] + \
            self.dtf_cases["Country/Region"].unique().tolist()

    @staticmethod
    def group_by_country(dtf, country):
        dtf = dtf.drop(['Province/State', 'Lat', 'Long'],
                       axis=1).groupby("Country/Region").sum().T
        dtf["World"] = dtf.sum(axis=1)
        dtf = dtf[country]
        dtf.index = pd.to_datetime(dtf.index, infer_datetime_format=True)
        ts = pd.DataFrame(index=dtf.index, data=dtf.values, columns=["data"])
        return ts

    def process_data(self, country):
        self.dtf = self.group_by_country(self.dtf_cases, country)
