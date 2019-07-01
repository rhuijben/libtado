from libtado.api import Tado

t = Tado(sys.argv[1], sys.argv[2], sys.argv[3])

#print(t.get_me())
#print(t.get_home())
print(t.get_zones())
#print(t.get_state(1))
#print(t.get_mobile_devices())
