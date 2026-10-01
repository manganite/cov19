from application.dash import app
from settings import config

app.run(debug=config.debug, host=config.host, port=config.port)
