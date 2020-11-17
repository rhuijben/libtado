#! /usr/bin/env python3

from libtado.api import Tado
import sys, getopt, os, datetime
from datetime import datetime
from dateutil.parser import parse
from dateutil import tz

zone_map = { 'D': 3, 'P' : 4, 'R' : 1, 'B': 2, 'T' : 7, 'J' : 6}
reverse_zone_map = {}
zone_info = {}
t = None

def time_str(time_str):
  given_time = parse(time_str).astimezone(tz.tzlocal())
  now = datetime.now().replace(tzinfo=tz.tzlocal())

  if (given_time - now).days < 1:
    return given_time.strftime('%H:%M') # As Time
  elif (given_time - now).days < 7:
    return given_time.strftime('%A') # Monday,..
  else:
    return given_time.strftime('%Y-%-m-%-d')

def zone_name(zone):
  global zone_map, zone_info

  if not zone_info:
    zone_info = t.get_zones()

  if zone in zone_map:
    zone = zone_map[zone]

  for z in zone_info:
    if int(z['id']) == zone:
      return z['name']


def show_help():
  print('My Tado Manager 0.0.1 beta 1')
  print('Usage td-mgr <args>')
  print('-l               List status (when done processing)')
  print('-v               Turn op verbose level (can be specified more than once)')
  print('-z <nr|letter>   Select specific zone(s)')
  print()
  print('-t <centigrade>  Set temperature in zone(s) to specific temperature')
  print('                 (Use temp <= 5 to set radiator to OFF)')
  print('-r               Reset zone(s) to tado-programming')
  print()
  print('Additional settings for setting temperature')
  print('-k               Make the specified temperature override all future programming')
  print('-x <minutes> 		Keep the specified setting for this number of minutes')
  print()


def show_list(verbose):
  global zone_info

  if not zone_info:
    zone_info = t.get_zones()

  for i in zone_info:
    st = t.get_state(i['id'])

    zone = i['id']

    if zone in reverse_zone_map:
      zone = reverse_zone_map[zone]

    if verbose > 0:
      print(i)
      print(st)

    cur_temp = st['sensorDataPoints']['insideTemperature']['celsius']
    cur_hum =  st['sensorDataPoints']['humidity']['percentage']

    if st['link']['state'] != 'ONLINE':
      setting = '-x-'
    elif st['setting']['power'] != 'ON':
      setting = st['setting']['power'][:3]
    else:
      setting = '%4.1fC' % (st['setting']['temperature']['celsius'])

    type_s = ''
    if st['overlayType'] and st['tadoMode'] != 'AWAY':
      type_s = st['overlayType']
    elif st['tadoMode'] != 'HOME':
      type_s = st['tadoMode'];

    next_s = ''

    if st['tadoMode'] != 'AWAY':
      if st['overlay'] != None:
        if 'termination' in st['overlay'] and st['overlay']['termination']['type'] == 'MANUAL':
          next_s = '-+-'
        elif st['overlay']['termination']['projectedExpiry'] != None:
          next_s = '-' + ('%s' % time_str(st['overlay']['termination']['projectedExpiry']))
        else:
          next_s = '-+-'
      elif st['nextScheduleChange'] != None:
        next_s = '-' + ('%s' % time_str(st['nextScheduleChange']['start']))

    extra = ''

    if st['openWindow'] != None:
      extra += ' Window open'
    for d in i['devices']:
      if d['batteryState'] != 'NORMAL':
        extra += ' Battery %s %s' % (d['serialNo'], d['batteryState'])

    heat_s = int(st['activityDataPoints']['heatingPower']['percentage'])

    if heat_s == 0:
      heat_s = ''
    else:
      heat_s = '%i%%' % heat_s

    print('%s %-12s %3s %5s %-8s %6s  %3.2fC %3.1f%%%s' % (zone, i['name'], heat_s, setting, next_s, type_s, cur_temp, cur_hum, extra))


def set_temperature(zones, temp, set_termination):
  global t, reverse_zone_map

  for z in zones:
    if temp >= 1:
      print("%s set to %0.1fC" % (zone_name(z), temp))
      r = t.set_temperature(z, temp, termination=set_termination)
      if not 'type' in r:
        print(r)
        sys.exit(1)
    else:
      print("%s reset to tado schedule" % (zone_name(z)))
      r = t.end_manual_control(z)
      if not r == None:
        print(r)
        sys.exit(1)


def main(argv):

  global t, zone_info

  t = Tado(os.getenv('TADO_USERNAME'), os.getenv('TADO_PASSWORD'), os.getenv('TADO_CLIENT_SECRET'))

  opts, args = getopt.getopt(argv,"hvlkrz:t:x:")

  verbose = 0

  for i in zone_map:
    reverse_zone_map[zone_map[i]] = i

  zones = []
  set_termination = 'AUTO'
  do_list = False
  set_temp = None

  for opt, arg in opts:
    if opt == '-h':
      show_help()
      sys.exit()
    elif opt == '-v':
      verbose += 1
    elif opt == '-z':
      if arg in zone_map:
        arg = zone_map[arg]

      zones += [int(arg)]
    elif opt == '-k':
      set_termination = 'MANUAL'
    elif opt == '-x':
      set_termination = int(arg) * 60
    elif opt == '-l':
      do_list = True

    elif opt == '-t':
      set_temp = float(arg)
      if set_temp < 1:
        set_temp = 1

    elif opt == '-r':
      set_temp = -1


  if set_temp != None and not zones:
    if not zone_info:
      zone_info = t.get_zones()

    for z in zone_info:
      zones += [int(z['id'])]

  if set_temp != None:
    set_temperature(zones, set_temp, set_termination)

  if do_list:
    show_list(verbose)


if __name__ == "__main__":
   main(sys.argv[1:])
