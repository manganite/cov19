Simple Covid-19 dashboard.

Based on a tutorial by Mauro Di Pietro at towardsdatascience.com:

https://towardsdatascience.com/how-to-embed-bootstrap-css-js-in-your-python-dash-app-8d95fc9e599e

Data provided by Johns Hopkins CSSE:

https://github.com/CSSEGISandData/COVID-19

## Data range

JHU CSSE stopped reporting recovered cases on 2021-08-05 and froze the whole
dataset on 2023-03-10. Active cases are derived from recovered cases, so the
dashboard uses data up to 2021-08-04 (`end_date` in `settings/config.py`) and
extrapolates 30 days from there.

## Static version (GitHub Pages)

Because the data no longer changes, `build_static.py` precomputes every
country and writes a server-less site to `site/`: one JSON file per country,
rendered in the browser with Plotly.js. The workflow in
`.github/workflows/pages.yml` builds and deploys it on every push to `master`.
GitHub Pages must be enabled once under *Settings → Pages → Source: GitHub
Actions*.

Build and preview locally (Python 3.12):

    pip install -r requirements.txt
    python build_static.py
    python -m http.server -d site 8000

## Dash app

The original interactive app still runs locally:

    pip install -r requirements.txt
    python run.py

Dependencies are declared in `requirements.in` and pinned in
`requirements.txt` with `uv pip compile requirements.in --python-version 3.12 -o requirements.txt`.
