import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties

# Location coordinates
latitude = xx
longitude = yy

# Forecast range
start_date = "2025-05-03"
end_date = "2025-05-06"


url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    f"&hourly=precipitation"
    f"&start_date={start_date}&end_date={end_date}"
    f"&timezone=auto"
    f"&model=icon"
)

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    timestamps = data['hourly']['time']
    rainfall = data['hourly']['precipitation']

    # Convert to datetime objects
    times = [datetime.fromisoformat(t) for t in timestamps]

    # Group into 6-hour intervals
    rainfall_6hr = []
    time_6hr = []

    for i in range(0, len(rainfall), 6):
        chunk = rainfall[i:i+6]
        avg_rain = np.mean(chunk)
        rainfall_6hr.append(avg_rain)
        time_6hr.append(times[i])

    # Normalize rainfall for colormap
    norm = mcolors.Normalize(vmin=min(rainfall_6hr), vmax=max(rainfall_6hr))
    cmap = cm.get_cmap("Blues")
    colors = [cmap(norm(val)) for val in rainfall_6hr]

    # Format datetime for x-axis
    time_labels = [dt.strftime("%b %d\n%H:%M") for dt in time_6hr]

    # Plotting
    #plt.figure(figsize=(12, 5))
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.bar(time_6hr, rainfall_6hr, color=colors, width=0.1)
    #plt.bar(time_6hr, rainfall_6hr, color=colors, width=0.1, align='center')

     # Format major ticks: every day
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

    # Format minor ticks: every 6 hours
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))

    # Rotate and show both major & minor tick labels
    plt.setp(ax.get_xticklabels(minor=False), rotation=90)
    plt.setp(ax.get_xticklabels(minor=True), rotation=90)

    # Bold font for major ticks (dates)
    bold_font = FontProperties(weight='bold')
    for label in ax.get_xticklabels(minor=False):
        label.set_fontproperties(bold_font)

    # Make sure minor ticks are visible
    ax.tick_params(axis='x', which='minor', length=5)
    ax.tick_params(axis='x', which='major', length=10)


    plt.xlabel("Date and Time")
    plt.ylabel("6-hour Avg Rainfall (mm)")
    plt.title(f"6-hour Rainfall Averages in Kammasandra:(using model updated at 0530hrs IST, open-meteo API/ICON). Next update time 1730hrs : dominic.chandar@gmail.com")
    #plt.xticks(rotation=45)
    
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("Failed to retrieve data:", response.status_code, response.text)
