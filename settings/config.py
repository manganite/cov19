import os

# App settings
name = "Covid-19 Data"

host = "0.0.0.0"

port = int(os.environ.get("PORT", 5000))

debug = False

data = "https://github.com/CSSEGISandData/COVID-19"

code = "https://github.com/mdipietro09/App_VirusForecaster"

# JHU CSSE stopped reporting recovered cases on 2021-08-05 (the series drops
# to zero afterwards) and froze the whole dataset on 2023-03-10. Active cases
# are derived from recovered, so the analysis ends on the last complete day.
end_date = "2021-08-04"

fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

# File system
root = os.path.dirname(os.path.dirname(__file__)) + "/"
