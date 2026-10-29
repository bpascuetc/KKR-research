"""Lab 17: public FRED current observations versus ALFRED date vintages."""
from datetime import date, datetime, timezone
from io import StringIO
import re
import ssl
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd
import streamlit as st
import certifi

NAMES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
DISCLAIMER = "I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own."


def validate_id(series_id):
    series_id = series_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_]+", series_id):
        raise ValueError("Use a FRED series ID containing letters, numbers or underscores.")
    return series_id


def parse_csv(raw):
    frame = pd.read_csv(StringIO(raw), na_values=["."])
    if len(frame.columns) != 2:
        raise ValueError("Expected one date column and one observation column.")
    dates = pd.to_datetime(frame.iloc[:, 0], errors="raise")
    values = pd.to_numeric(frame.iloc[:, 1], errors="raise")
    result = pd.Series(values.to_numpy(), index=dates, name="value").dropna().sort_index()
    if result.empty or result.index.has_duplicates:
        raise ValueError("No valid observations, or duplicate observation dates.")
    return result


def fetch(url):
    request = Request(url, headers={"User-Agent": "FIN43900-Lab17/1.0"})
    with urlopen(request, timeout=45, context=ssl.create_default_context(cafile=certifi.where())) as response:
        raw = response.read().decode("utf-8-sig")
    return {"values": parse_csv(raw), "raw": raw, "url": url,
            "downloaded_utc": datetime.now(timezone.utc).isoformat()}


@st.cache_data(ttl=3600, show_spinner=False)
def download_current(series_id):
    series_id = validate_id(series_id)
    return fetch("https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode({"id": series_id}))


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known(series_id, as_known):
    series_id = validate_id(series_id)
    vintage = date.fromisoformat(str(as_known))
    if vintage > date.today():
        raise ValueError("An as-known date cannot be in the future.")
    # ALFRED selects the historical version on the server. Filtering current
    # observations by observation date would NOT reproduce that information set.
    url = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?" + urlencode(
        {"id": series_id, "vintage_date": vintage.isoformat()})
    result = fetch(url)
    if (result["values"].index.date > vintage).any():
        raise ValueError("Vintage response contains future observation dates; refusing it.")
    return result


def comparison(series_id, current, vintage, start):
    current = current.loc[pd.Timestamp(start):]
    vintage = vintage.loc[pd.Timestamp(start):]
    common = current.index.intersection(vintage.index)
    revisions = (current.loc[common] - vintage.loc[common]).abs() > 1e-9
    last_known = None if vintage.empty else vintage.index[-1]
    return {
        "Series": series_id, "FRED page": "https://fred.stlouisfed.org/series/" + series_id,
        "Last measured, as known": last_known,
        "Value, as known": None if vintage.empty else float(vintage.iloc[-1]),
        "Last measured, current": None if current.empty else current.index[-1],
        "Value, current": None if current.empty else float(current.iloc[-1]),
        "Later observations": None if last_known is None else int((current.index > last_known).sum()),
        "Revised common dates": int(revisions.sum()),
        "Common dates compared": len(common),
    }


def main():
    st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")
    st.title("Point-in-Time Rates Audit")
    st.caption("Data from FRED and ALFRED, Federal Reserve Bank of St. Louis; downloaded on the dates shown below. Built with AI help; a learning demonstration, not investment advice.")
    selected = st.sidebar.multiselect("Series", list(NAMES), default=list(NAMES),
                                     format_func=lambda x: f"{x} — {NAMES[x]}")
    extra = st.sidebar.text_input("Add another FRED series ID", value="")
    start = st.sidebar.date_input("Start date", date(2020, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())
    as_known = st.sidebar.date_input("As known on", date.today(), min_value=date(1900, 1, 1), max_value=date.today())
    if st.sidebar.button("Refresh downloads"):
        st.cache_data.clear()
    st.info("Vintage dates are daily, not intraday trade timestamps. Counts use the selected observation window. Missing values are excluded; no forward filling.")
    if start > as_known:
        st.warning("Start date is after the as-known date; that vintage may have no observations in this window.")
    if extra.strip():
        selected = list(dict.fromkeys(selected + [extra.strip().upper()]))
    rows = []
    for series_id in selected:
        st.subheader(f"{series_id} — {NAMES.get(series_id, 'Additional series')}")
        try:
            with st.spinner(f"Downloading {series_id}…"):
                now = download_current(series_id)
                then = download_as_known(series_id, as_known)
            row = comparison(series_id, now["values"], then["values"], start)
            rows.append(row)
            plot = pd.concat({"Current": now["values"], "As known": then["values"]}, axis=1).loc[pd.Timestamp(start):]
            st.line_chart(plot, x_label="Observation date", y_label="Published series units (see FRED page)")
            last = row["Last measured, as known"]
            st.write("Last measured date known then: " + ("None in this window" if last is None else last.strftime("%Y-%m-%d")))
            st.caption(f"Current download UTC: {now['downloaded_utc']} · Vintage download UTC: {then['downloaded_utc']}")
            st.markdown(f"[FRED series page]({row['FRED page']}) · [Current CSV]({now['url']}) · [Vintage CSV]({then['url']})")
        except Exception as exc:
            st.error(f"{series_id}: {type(exc).__name__}: {exc}")
    if rows:
        st.subheader("Point-in-time comparison")
        st.dataframe(pd.DataFrame(rows), hide_index=True, column_config={
            "FRED page": st.column_config.LinkColumn("FRED page")})
        st.caption("Later observations are dated after the last measured observation available then. Revisions compare only dates with valid values in BOTH downloads; a new observation is not a revision. An empty vintage has an unavailable later-count, not zero.")
    st.caption(DISCLAIMER)


if __name__ == "__main__":
    main()
