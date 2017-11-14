# encoding: utf-8
from collections import deque
from datetime import date, timedelta

from astral import Astral, Location, SUN_RISING, SUN_SETTING
from icalendar import Calendar, Event


def sliding_window(iterable, n):
    items = deque(maxlen=n)
    for _ in range(n):
        items.append(next(iterable))
    yield tuple(items)
    for item in iterable:
        items.append(item)
        yield tuple(items)


def make_event(title, start, end):
    ev = Event()
    ev.add('summary', title)
    ev.add('dtstart', start)
    ev.add('dtend', end)
    return ev


def make_events(city, today, tomorrow):
    #sunset = city.sunset(date=today)
    dusk = city.dusk(date=today)
    dawn = city.dawn(date=tomorrow)
    #sunrise = city.sunrise(date=tomorrow)
    #yield make_event('Hämärä', sunset, dusk)
    yield make_event('Pimeä', dusk, dawn)
    #yield make_event('Hämärä', dawn, sunrise)


def write(cal):
    with open('out.ics', 'w') as f:
        f.write(cal.to_ical())


def make_cal(city, dates):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for today, tomorrow in sliding_window(dates, 2):
        for ev in make_events(city, today, tomorrow):
            cal.add_component(ev)

    return cal


def main():
    a = Astral()
    a.solar_depression = 'civil'
    # city = a['Helsinki']
    city = Location(('Koti', 'Finland', 60.191095,
                     24.802785, 'Europe/Helsinki', 10))
    city.sun()
    start = date.today()
    dates = (start + timedelta(days=k) for k in range(1, 90))

    write(make_cal(city, dates))


if __name__ == '__main__':
    main()
