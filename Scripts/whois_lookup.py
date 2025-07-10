import socket
from datetime import date
from datetime import timedelta


today = date.today()
yesterday = today - timedelta(days = 1)


def domain_lookup(dm: str):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("whois.iana.org", 43))
	s.send(f"{dm}\r\n".encode())
	response = s.recv(4096).decode()
	s.close()
	return response


def main():
	with open("YOUR_PATH"+ str(yesterday) + ".txt" , "r") as f:
		domain_names = f.readlines()

	for domain_name in domain_names:
		domain_name = domain_name.strip()
		info = domain_lookup(domain_name)

		with open("YOUR_PATH"+str(yesterday)+".txt", "a") as outfile:
			outfile.write("Domain: "+ domain_name + "\nWHOIS info:\n" + info + "\n")


if __name__ == "__main__":
	main()
