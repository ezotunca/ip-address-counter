ip_counts = {}

with open("sample.log", "r") as log_file:
    for line in log_file:
        parts = line.split()
        ip = parts[-1]

        if ip in ip_counts:
            ip_counts[ip] += 1
        else:
            ip_counts[ip] = 1

print("IP Address Count:")
for ip, count in ip_counts.items():
    print(ip, "-", count)
