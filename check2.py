import sys
import os
import json
import datetime
from libtado.api import Tado

def print_d(data):
  print(json.dumps(data, indent=2))

TADO_USERNAME = os.getenv("TADO_USERNAME")
TADO_PASSWORD = os.getenv("TADO_PASSWORD")
TADO_CLIENT_SECRET = os.getenv("TADO_CLIENT_SECRET")

tado = Tado(TADO_USERNAME, TADO_PASSWORD, TADO_CLIENT_SECRET)

print('--me')
me = tado.get_me()
print_d(me)

print('--home')
home = tado.get_home()
print_d(home)

print('--home_state')
print_d(tado.get_home_state())

print('--installations')
print_d(tado.get_installations())

print('--users')
print_d(tado.get_users())

print('--heating_ciruits')
print_d(tado.get_heating_circuits())

print('--incidents')
print_d(tado.get_incidents())

print('--installations')
print_d(tado.get_installations())

print('--zones')
zones = tado.get_zones()
print_d(zones)
zone_id = int(zones[0]['id'])

print('--(zone_)capabilities %i' % zone_id)
print_d(tado.get_capabilities(zone_id))

print('--(zone_)default_overlay %i' % zone_id)
print_d(tado.get_default_overlay(zone_id))

print('--(zone_)state %i' % zone_id)
print_d(tado.get_state(zone_id))

print('--(zone_)early_start %i' % zone_id)
print_d(tado.get_early_start(zone_id))

print('--(zone_)measuring_device %i' % zone_id)
print_d(tado.get_measuring_device(zone_id))

print('--(zone_)away_configuration %i' % zone_id)
print_d(tado.get_away_configuration(zone_id))

today_str = str(datetime.date.today())
print('--(zone_)report %i %s' % (zone_id, today_str))
print_d(tado.get_report(zone_id, today_str))

print('--schedule_timetables %i' % zone_id)
print_d(tado.get_schedule_timetables(zone_id))

print('--schedule %i' %zone_id)
schedule_timetable = tado.get_schedule(zone_id)
print_d(schedule_timetable)
schedule_id = int(schedule_timetable['id'])

print('--schedule_blocks %i %i' % (zone_id, schedule_id))
print_d(tado.get_schedule_blocks(zone_id, schedule_id))

print('--devices')
devices = tado.get_devices()
print_d(devices)

print('--device_usage')
print_d(tado.get_device_usage())

print('--get_temperature_offset %s' % devices[-1]['shortSerialNo'])
print_d(tado.get_temperature_offset(devices[-1]['shortSerialNo']))

print('--mobile_devices')
print_d(tado.get_mobile_devices())
