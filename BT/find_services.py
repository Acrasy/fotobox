import bluetooth


devices=bluetooth.discover_devices(lookup_names=True)
print(type(devices))

print("Devices found: %s" %len(devices))

for item in devices:
	print(item)


services= bluetooth.find_service()


for i in range(len(services)):
	name = str(services[i]["name"])
	port = str(services[i]["port"])
	host = str(services[i]["host"])

	print("name: " + name)
	print("port: " + port)
	print("host: " + host)


