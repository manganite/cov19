import numpy as np
import pandas as pd
from scipy import optimize


class Model():

    def __init__(self, dtf):
        self.dtf = dtf

    @staticmethod
    def f(X, c, k, m):
        y = c / (1 + np.exp(-k*(X-m)))
        return y

    @staticmethod
    def fit_parametric(X, y, f, p0):
        # The default guess (rate 1/day, midpoint at day 1) fails to converge
        # for countries still in exponential growth at the end of the data.
        # Retry with a slow rate and a midpoint beyond the last data point.
        fallbacks = [[2*np.max(y), 0.05, len(y)], [10*np.max(y), 0.05, len(y)+60]]
        for guess in [p0] + fallbacks:
            try:
                model, cov = optimize.curve_fit(f, X, y, maxfev=10000, p0=guess)
                return model
            except RuntimeError:
                continue
        raise RuntimeError("logistic fit did not converge for any initial guess")

    @staticmethod
    def forecast_parametric(model, f, X):
        preds = f(X, model[0], model[1], model[2])
        return preds

    @staticmethod
    def generate_indexdate(start):
        index = pd.date_range(start=start, periods=30, freq="D")
        index = index[1:]
        return index

    @staticmethod
    def add_diff(dtf):
        # create delta columns
        dtf["delta_data"] = dtf["data"] - dtf["data"].shift(1)
        dtf["delta_forecast"] = dtf["forecast"] - dtf["forecast"].shift(1)

        # fill Nas
        dtf["delta_data"] = dtf["delta_data"].bfill()
        dtf["delta_forecast"] = dtf["delta_forecast"].bfill()

        # interpolate outlier
        idx = dtf[pd.isnull(dtf["data"])]["delta_forecast"].index[0]
        posx = dtf.index.tolist().index(idx)
        posx_a = posx - 1
        posx_b = posx + 1
        col = dtf.columns.get_loc("delta_forecast")
        dtf.iloc[posx, col] = (
            dtf.iloc[posx_a, col] + dtf.iloc[posx_b, col])/2
        return dtf

    def forecast(self, mortality):
        # fit active cases
        y = self.dtf["data"].values
        t = np.arange(len(y))
        model = self.fit_parametric(t, y, self.f, p0=[np.max(y), 1, 1])
        fitted = self.f(t, model[0], model[1], model[2])
        self.dtf["forecast"] = fitted

        # forecast active cases
        t_ahead = np.arange(len(y), len(y)+29)
        forecast_active = self.forecast_parametric(model, self.f, t_ahead)

        # fit recovered
        y = self.dtf["recovered"].values
        model = self.fit_parametric(t, y, self.f, p0=[np.max(y), 1, 1])

        # forecast recovered
        forecast_recovered = self.forecast_parametric(model, self.f, t_ahead)

        # create dtf
        self.today = self.dtf.index[-1]
        idxdates = self.generate_indexdate(start=self.today)
        data = {'forecast': list(forecast_active),
                'recovered': list(forecast_recovered)}
        preds = pd.DataFrame(
            data=data,
            index=idxdates
        )
        self.dtf = pd.concat([self.dtf, preds])

        # add diff
        self.dtf = self.add_diff(self.dtf)

        # add deaths
        self.dtf["deaths"] = self.dtf["deaths"].fillna(
            mortality * self.dtf["forecast"])

        # add active
        self.dtf["active"] = self.dtf["active"].fillna(
            self.dtf["forecast"] - self.dtf["recovered"] - self.dtf["deaths"])
