import os

# App settings
name = "Covid-19 Data"

host = "0.0.0.0"

port = int(os.environ.get("PORT", 5000))

debug = False

data = "https://github.com/CSSEGISandData/COVID-19"

code = "https://github.com/mdipietro09/App_VirusForecaster"

fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

# File system
root = os.path.dirname(os.path.dirname(__file__)) + "/"
