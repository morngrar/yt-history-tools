#!/usr/bin/python

"""
Plots the out.csv as a SCC
"""


from datetime import datetime, date
from matplotlib import pyplot as plt
import numpy as np

DAILY = 0
WEEKLY = DAILY+1
MONTHLY = WEEKLY+1
YEARLY = MONTHLY+1

PERIOD = WEEKLY
#GOAL = 70
GOAL = 15
#LIMIT = date(2020,12,1)
LIMIT = date(2010,12,1)

def add_phase(ax, x, y, text, rotation=76):
    if x != 0:
        ax.axvline(x, color="grey", ls="--")

    ax.text(x, y, text, rotation=rotation, color="grey")


def get_date(stamp):
    tmp = datetime.strptime(stamp, "%b %d, %Y, %I:%M:%S\u202f%p %Z")

    if PERIOD == DAILY:
        return date(tmp.year, tmp.month, tmp.day)

    if PERIOD == WEEKLY:
        weekday = tmp.isocalendar()
        monday = date.fromisocalendar(weekday[0], weekday[1], 1)
        return monday

    if PERIOD == MONTHLY:
        return date(tmp.year, tmp.month, 1)

    if PERIOD == YEARLY:
        return date(tmp.year, 1, 1)



def main():
    import csv

    # read csv
    rows = []
    with open("out.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    rows = rows[1:] # drop titles
    rows.reverse()

    # removes non-breaking space characters from timestamps
    rows = [[row[0].replace("\u202f", " "), row[1]] for row in rows]

    # only keep new dates
    rows = [
        row for row in rows
        if get_date(row[0]) >= LIMIT
    ]

#    normal = [row for row in rows if "#short" not in row[1]]
    shorts = [row for row in rows if "#short" in row[1]]

    print("generating howto list")
    howto = [
        row for row in rows 
        if "how to" in row[1].lower() or "howto" in row[1].lower() or "how-to" in row[1].lower()
    ]

    howto_counts = {}
    last = ""
    print("counting howtos")
    for row in howto:
        day = get_date(row[0]).isoformat()
        if day != last:
            last = day
            howto_counts[last] = 0
        howto_counts[last] += 1

    # accumulate normal per day
#    normal_counts = {}
#    last = ""
#    for row in normal:
#        day = get_date(row[0]).isoformat()
#        if day != last:
#            last = day
#            normal_counts[last] = 0
#        normal_counts[last] += 1

    # accumulate shorts per day
    shorts_counts = {}
    last = ""
    print("counting shorts")
    for row in shorts:
        day = get_date(row[0]).isoformat()
        if day != last:
            last = day
            shorts_counts[last] = 0
        shorts_counts[last] += 1

    # accumulate total per day
    total_counts = {}
    last = ""
    print("counting totals")
    for row in rows:
        day = get_date(row[0]).isoformat()
        if day != last:
            last = day
            total_counts[last] = 0
        total_counts[last] += 1



    fig, ax = plt.subplots(1,1)
    ax.set_yscale("log")

    #add_celeration_angles(ax, length, min_value, max_value)

    # phases
#    short_intro_date = datetime(2021, 6, 13)
#    add_phase(ax, short_intro_date, 4, "Shorts release")

    add_phase(ax, datetime(2023, 2, 10), 2, "start measurement")


    add_phase(ax, datetime(2023, 4, 24), 2, "lowered goal from 70 to 15 per week")

    add_phase(ax, datetime(2023, 5, 31), 2, "delivered MACS")
    
    # goal
    plt.axhline(70, ls="--", color="#aac", label="First weekly goal")
    plt.axhline(GOAL, color="orange", label="Weekly goal")
    plt.axhline(3, color="green", label="Daily goal")

    # plot values
#    xs = [date.fromisoformat(k) for k in normal_counts.keys()]
#    ys = [v for v in normal_counts.values()]
#    ax.plot(xs, ys, "o", ms=3, color="cyan", label="Normal")

    print("plotting totals")
    xs = [date.fromisoformat(k) for k in total_counts.keys()]
    ys = [v for v in total_counts.values()]
    ax.plot(xs, ys, "o", ms=3, color="blue", label="All")

    print("plotting shorts")
    xs = [date.fromisoformat(k) for k in shorts_counts.keys()]
    ys = [v for v in shorts_counts.values()]
    ax.plot(xs, ys, "o", ms=3, color="red", label="Shorts")

#    print("plotting howtos")
#    xs = [date.fromisoformat(k) for k in howto_counts.keys()]
#    ys = [v for v in howto_counts.values()]
#    ax.plot(xs, ys, "o", ms=3, color="red", label="Howtos")
    
    period = "N/A"
    if PERIOD == DAILY:
        period = "day"
    elif PERIOD == WEEKLY:
        period = "week"
    elif PERIOD == MONTHLY:
        period = "month"

    ax.set_ylabel(f"Views per {period}")
    ax.set_xlabel("Time")

    plt.grid(True, which="both")
    plt.grid(which='major',axis ='y', linewidth='1', color='black')
    plt.grid(which='major',axis ='x', linewidth='1')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='grey')
    ax.legend()



    # x-axis gridlines
    from matplotlib.dates import DayLocator, WeekdayLocator
    from matplotlib import dates
    #ax.minorticks_on()
    #ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_minor_locator(WeekdayLocator(byweekday=[dates.MO]))



    plt.show()








if __name__=="__main__":
    main()

