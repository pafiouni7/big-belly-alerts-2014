# Big Belly Alerts & Locations (Streamlit)

This Streamlit app explores **2014 Big Belly Alert** data using an interactive **map** plus summary **charts**.

It includes:
- **Map (PyDeck):** plots the locations of Big Belly Alerts (lat/long parsed from the `location` column).
- **Pie chart (Matplotlib):** percentage breakdown of selected **description** values (based on selected fullness color).
- **Bar chart #1 (Matplotlib):** counts of selected **description** values (based on selected fullness color).
- **Bar chart #2 (Matplotlib):** counts of **fullness** values (GREEN/YELLOW/RED), color-coded.

A sidebar lets you:
- **Multiselect descriptions** to include in the pie/bar charts
- **Radio select a fullness color** (Green/Yellow/Red) that filters the data used in the pie chart + first bar chart

---

## Requirements

- Python 3.9+ recommended
- Packages:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `pydeck`

Install:

```bash
pip install streamlit pandas numpy matplotlib pydeck

