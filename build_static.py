"""Build a static version of the dashboard for GitHub Pages.

The JHU CSSE data is frozen, so every country's figures and panel values can
be computed once at build time. The page then needs no server: it loads one
JSON file per country and renders it with Plotly.js.

Usage: python build_static.py [output_dir]   (default: site/)
"""
import json
import re
import shutil
import sys
import warnings
from pathlib import Path

import plotly
import plotly.io as pio

from python.data import Data
from python.model import Model
from python.result import Result
from settings import about, config

ROOT = Path(__file__).resolve().parent


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def figure_json(fig):
    # The dark template is identical for every figure, so it is shipped once
    # in index.html instead of being repeated in each of ~800 figures.
    spec = json.loads(fig.to_json())
    spec["layout"].pop("template", None)
    return spec


def country_payload(data, country):
    data.process_data(country)
    model = Model(data.dtf)
    model.forecast(data.mortality)
    result = Result(model.dtf)
    peak_day, num_max, total_today, total_30, active_today, active_30 = result.get_panel()
    return {
        "country": country,
        "figures": {
            "cumulative": figure_json(result.plot_cumulative()),
            "relative": figure_json(result.plot_relative()),
            "model": figure_json(result.plot_total(model.today)),
            "daily": figure_json(result.plot_active(model.today)),
        },
        "panel": {
            "total_cases_until_today": float(total_today),
            "total_cases_in_30days": float(total_30),
            "active_cases_today": float(active_today),
            "active_cases_in_30days": float(active_30),
            "peak_day": peak_day.strftime("%Y-%m-%d"),
            "peak_cases": float(num_max),
            "peak_passed": bool(model.today >= peak_day),
        },
    }


def main(out_dir):
    out = Path(out_dir)
    if out.exists():
        shutil.rmtree(out)
    (out / "data").mkdir(parents=True)

    data = Data()
    data.get_data()

    countries = []
    for country in data.countrylist:
        # curve_fit warns about overflow in exp() while it explores the
        # parameter space; the converged fits are unaffected.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            payload = country_payload(data, country)
        slug = slugify(country)
        (out / "data" / f"{slug}.json").write_text(json.dumps(payload, separators=(",", ":")))
        countries.append({"name": country, "slug": slug})
    print(f"built {len(countries)} countries")

    template_layout = pio.templates["plotly_dark"].layout.to_plotly_json()
    index = (ROOT / "static_site" / "index.html").read_text()
    index = (index
             .replace("__TITLE__", config.name)
             .replace("__END_DATE__", config.end_date)
             .replace("__ABOUT__", about.txt)
             .replace("__DATA_URL__", config.data)
             .replace("__CODE_URL__", config.code)
             .replace("__COUNTRIES__", json.dumps(countries))
             .replace("__TEMPLATE__", json.dumps(template_layout)))
    (out / "index.html").write_text(index)

    plotly_js = Path(plotly.__file__).parent / "package_data" / "plotly.min.js"
    shutil.copy(plotly_js, out / "plotly.min.js")
    shutil.copy(ROOT / "application" / "static" / "favicon.ico", out / "favicon.ico")
    (out / ".nojekyll").touch()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "site")
