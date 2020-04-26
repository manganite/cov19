import pandas as pd
import plotly.graph_objects as go


class Result():

    def __init__(self, dtf):
        self.dtf = dtf

    @staticmethod
    def calculate_peak(dtf):
        data_max = dtf["delta_data"].max()
        forecast_max = dtf["delta_forecast"].max()
        if data_max >= forecast_max:
            peak_day = dtf[dtf["delta_data"] == data_max].index[0]
            return peak_day, data_max
        else:
            peak_day = dtf[dtf["delta_forecast"] == forecast_max].index[0]
            return peak_day, forecast_max

    @staticmethod
    def calculate_max(dtf):
        total_cases_until_today = dtf["data"].iat[-30]
        total_cases_in_30days = dtf["forecast"].iat[-1]
        active_cases_today = dtf["delta_data"].iat[-30]
        active_cases_in_30days = dtf["delta_forecast"].iat[-1]
        return total_cases_until_today, total_cases_in_30days, active_cases_today, active_cases_in_30days

    def plot_total(self, today):
        # main plots
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.dtf.index,
            y=self.dtf["data"],
            mode='markers',
            name='confirmed',
            marker_color='slategrey'
        ))

        fig.add_trace(go.Scatter(
            x=self.dtf.index,
            y=self.dtf["forecast"],
            mode='none',
            name='extrapolation',
            fill='tozeroy',
            fillcolor='rgba(140, 80, 180, 0.25)'
        ))

        fig.add_trace(go.Bar(
            x=self.dtf.index,
            y=self.dtf["active"],
            name='active',
            marker_color='royalblue'
        ))

        fig.add_trace(go.Bar(
            x=self.dtf.index,
            y=self.dtf["recovered"],
            name='recovered',
            marker_color='darkcyan'
        ))

        fig.add_trace(go.Bar(
            x=self.dtf.index,
            y=self.dtf["deaths"],
            name='deaths',
            marker_color='firebrick'
        ))

        # add slider
        fig.update_xaxes(
            rangeslider_visible=True
        )

        # set background color
        fig.update_layout(
            title="Extrapolation of cumulative data",
            template='plotly_dark',
            autosize=True,
            height=500
        )

        # add vline
        fig.add_shape({
            "x0": today,
            "x1": today,
            "y0": 0,
            "y1": self.dtf["forecast"].max(),
            "type": "line",
            "line": {"width": 2, "dash": "dot"}
        })
        fig.add_annotation(
            x=today,
            y=self.dtf["forecast"].max(),
            text="today",
            ax=-5,
            ay=-20
        )

        return fig

    def plot_active(self, today):
        # main plots
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=self.dtf.index,
            y=self.dtf["delta_data"],
            name='confirmed',
            marker_color='slategrey')
        )

        fig.add_trace(go.Scatter(
            x=self.dtf.index,
            y=self.dtf["delta_forecast"],
            mode='none',
            name='extrapolation',
            fill='tozeroy',
            fillcolor='rgba(120, 100, 170, 0.3)'
        ))

        # add slider
        fig.update_xaxes(
            rangeslider_visible=True
        )

        # set background color
        fig.update_layout(
            title="Daily cases",
            template='plotly_dark',
            autosize=True,
            height=500
        )

        # add vline
        fig.add_shape({
            "x0": today,
            "x1": today,
            "y0": 0,
            "y1": self.dtf["delta_forecast"].max(),
            "type": "line",
            "line": {"width": 2, "dash": "dot"}
        })
        fig.add_annotation(
            x=today,
            y=self.dtf["delta_forecast"].max(),
            text="today",
            ax=-5,
            ay=-20
        )

        return fig

    def plot_cumulative(self):
        # main plots
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.dtf.index[:-29],
            y=self.dtf["deaths"][:-29],
            name='deaths',
            marker_color='firebrick',
            fill='tonexty'
        ))

        fig.add_trace(go.Scatter(
            x=self.dtf.index[:-29],
            y=self.dtf["recovered"][:-29],
            name='recovered',
            marker_color='darkcyan',
            fill='tonexty'
        ))

        fig.add_trace(go.Scatter(
            x=self.dtf.index[:-29],
            y=self.dtf["active"][:-29],
            name='active',
            marker_color='royalblue',
            fill='tonexty'
        ))

        fig.add_trace(go.Scatter(
            x=self.dtf.index[:-29],
            y=self.dtf["data"][:-29],
            name='confirmed',
            marker_color='slategrey',
            fill='tonexty'
        ))

        # add slider
        fig.update_xaxes(
            rangeslider_visible=True
        )

        # set background color
        fig.update_layout(
            title="Cumulative data",
            template='plotly_dark',
            autosize=True,
            height=500
        )

        return fig

    def plot_relative(self):
        # main plots
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.dtf.index[:-29],
            y=100*self.dtf["deaths"][:-29]/self.dtf["data"][:-29],
            name='deaths',
            mode='lines',
            marker_color='firebrick',
            stackgroup='one'
        ))

        fig.add_trace(go.Scatter(
            x=self.dtf.index[:-29],
            y=100*self.dtf["recovered"][:-29]/self.dtf["data"][:-29],
            name='recovered',
            mode='lines',
            marker_color='darkcyan',
            stackgroup='one'
        ))

        fig.add_trace(go.Scatter(
            x=self.dtf.index[:-29],
            y=100*self.dtf["active"][:-29]/self.dtf["data"][:-29],
            name='active',
            mode='lines',
            marker_color='royalblue',
            stackgroup='one'
        ))

        # add slider
        fig.update_xaxes(
            rangeslider_visible=True
        )

        # set background color
        fig.update_layout(
            title="Relative data",
            template='plotly_dark',
            autosize=True,
            height=500,
            yaxis=dict(type='linear', range=[0, 100], ticksuffix='% ')
        )

        return fig

    def get_panel(self):
        peak_day, num_max = self.calculate_peak(self.dtf)
        total_cases_until_today, total_cases_in_30days, active_cases_today, active_cases_in_30days = self.calculate_max(
            self.dtf)
        return peak_day, num_max, total_cases_until_today, total_cases_in_30days, active_cases_today, active_cases_in_30days
