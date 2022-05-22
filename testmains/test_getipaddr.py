import socket

ip = socket.gethostbyname('lita.local')
print(f"lita.local:  {ip}")

localhost = socket.gethostname()
print(f"localhost:  {localhost}")

hostinfo = socket.getaddrinfo("lita.local", 80)
print (hostinfo)
for item in hostinfo:
	print("  ", item)
