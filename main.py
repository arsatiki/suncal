# encoding: utf-8
from datetime import date, timedelta

from astral import Astral, Location, SUN_RISING, SUN_SETTING
from icalendar import Calendar, Event

def make_event(title, start, end):
    ev = Event()
    ev.add('summary', title)
    ev.add('dtstart', start)
    ev.add('dtend', end)
    return ev

def make_events(city, d):
    # d keys: dawn, sunrise, noon, sunset and dusk
    yield make_event('Hämärä', *city.twilight(date=d, direction=SUN_RISING))
    yield make_event('Hämärä', *city.twilight(date=d, direction=SUN_SETTING))
    yield make_event('Pimeä', *city.night(date=d))
               

def write(cal):
    with open('out.ics', 'w') as f:
        f.write(cal.to_ical())

def make_cal(city, dates):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for d in dates:
        for ev in make_events(city, d):
            cal.add_component(ev)

    return cal

def main():
    a = Astral()
    a.solar_depression = 'civil'
    # city = a['Helsinki']
    city = Location(('Koti', 'Finland', 60.191095, 24.802785, 'Europe/Helsinki', 10))
    city.sun()
    start = date(2017,10,16)
    dates = (start + timedelta(days=k) for k in range(1, 90))

    write(make_cal(city, dates))

if __name__ == '__main__':
    main()
