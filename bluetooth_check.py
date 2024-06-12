import bluetooth



##This is to check if the device is there.. comment out if you're not using (or put this in a separate file)
print("Performing inquiry...")
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print(f"Found {len(nearby_devices)} devices.")
for addr, name in nearby_devices:
    print(f"Address: {addr}, Name: {name}")




# Address: 00:24:01:01:04:7E, Name: TEAMG