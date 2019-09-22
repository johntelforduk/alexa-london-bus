# Test the bus stop API to text processing.

import bus_stop as bs

buses = bs.bus_arrivals(naptan_id='490014129N')

print(buses)
talk = bs.buses_to_speech(buses)
print(talk)
