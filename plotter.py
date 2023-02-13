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
GOAL = 70
LIMIT = date(2020,12,1)

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
    
    # goal
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



#    apply_scaling(
#        ax, length, min_value, max_value, divide_by_ten, lock_aspect=False
#    )

    plt.show()





def add_celeration_angles(ax, chart_length, min_value, max_value):

    upper_y = max_value/100 
    lower_y = min_value

    color = "#c4c4c4"
    
    start_session = chart_length//10-3

    def calc_text_x(offset):
        return 0.5+(start_session+offset)*10

    upper_text_y = upper_y*10 + upper_y

    ax.text(
        calc_text_x(1), 
        upper_text_y, 
        "x1.1", 
        color=color
    )
    x1_1 = displace_series(
        internal.genx(1.1, 10, start=upper_y), 
        start_session+1
    )
    ax.text(calc_text_x(2), upper_text_y, "x1.2", color=color)
    x1_2 = displace_series(
        internal.genx(1.2, 10, start=upper_y), 
        start_session+2
    )
    ax.text(calc_text_x(3),upper_text_y, "x1.3", color=color)
    x1_3 = displace_series(
        internal.genx(1.3, 10, start=upper_y), 
        start_session+3
    )

    lower_text_y = lower_y *10 +lower_y

    x1_5 = displace_series(
        internal.genx(1.5, 10, start=lower_y), 
        start_session+1
    )
    ax.text(calc_text_x(1), lower_text_y, "x1.5", color=color)
    x2 = displace_series(
        internal.genx(2, 10, start=lower_y), 
        start_session+2
    )
    ax.text(calc_text_x(2)+1, lower_text_y, "x2", color=color)
    x3 = displace_series(
        internal.genx(3, 10, start=lower_y), 
        start_session+3
    )
    ax.text(calc_text_x(3)+1, lower_text_y, "x3", color=color)

    ax.plot(x1_1, label="x1.1", lw=2.5, color=color)
    ax.plot(x1_2, label="x1.2", lw=2.5, color=color)
    ax.plot(x1_3, label="x1.3", lw=2.5, color=color)
    ax.plot(x1_5, label="x1.5", lw=2.5, color=color)
    ax.plot(x2, label="x2", lw=2.5, color=color)
    ax.plot(x3, label="x3", lw=2.5, color=color)

def apply_scaling(
    ax, length, min_value, max_value, divide_by_ten, lock_aspect=True
):
    scale_length = length+10
    scale = internal.apply_log_range(ax, min_value, max_value)
    internal.apply_xrange(ax, scale_length, divide_by_ten=divide_by_ten)
    plt.grid()

    if lock_aspect:
        internal.apply_scale_ratio(ax, scale)



if __name__=="__main__":
    main()

