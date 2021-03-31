# only needs to parse simplified json
import time
import re
from datetime import datetime, timedelta
from collections import OrderedDict

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] # 0-6 (0 is Monday)
timespan_parser = re.compile(r"(\d+):(\d+)\s?-\s?(\d+):(\d+)")

class Whatsnext:
    def __init__(self, schedule_base):
         self.schedule_base = schedule_base

    ### take a date as a struct_time
    def schedule(self, date, reverse=False):
        date = date.replace(second=0, microsecond=0)
        day_of_week = weekdays[date.weekday()]
        date_id = f"{date:%Y-%m-%d}"

        schedule = self.schedule_base.get(day_of_week, {})
        schedule = self.schedule_base.get(date_id, schedule).items()
        if reverse: schedule = reversed(list(schedule))

        for class_id, timespan in schedule:
            ts = list(map(int, timespan_parser.match(timespan).groups()))
            yield {
                'id': class_id,
                'start': date.replace(hour=ts[0], minute=ts[1]),
                'end': date.replace(hour=ts[2], minute=ts[3])
            }

    def classes(self, date, reverse=False):
        schedule = (period
            for period in self.schedule(date, reverse=reverse)
            if (not reverse and period['end'] > date) or
                   (reverse and period['end'] < date))
        while True:
            for period in schedule:
                yield period
            date += timedelta(days = 1 if not reverse else -1)
            schedule = self.schedule(date, reverse=reverse)

    def next(self, date):
        return next(self.classes(date))

    def prev(self, date):
        return next(self.classes(date, reverse=True))

if __name__ == "__main__":
    import json
    schedule_base = json.load(open("schedule_orig.json"))

    date = datetime.now()

    inst = Whatsnext(schedule_base)
    classes = inst.classes(date)

    for i in inst.schedule(date):
        print(i)

    #import whatsnext_test
