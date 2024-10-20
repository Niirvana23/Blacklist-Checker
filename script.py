import dns.resolver
import requests
import sys

# ===== Configuration Variables =====
# Webhook URL (replace this with your actual webhook URL)
WEBHOOK_URL = "https://example.com/webhook"

BLACKLIST_SERVICES = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "b.barracudacentral.org",
    "dnsbl.sorbs.net",
    "sbl.spamhaus.org",
    "xbl.spamhaus.org",
    "pbl.spamhaus.org",
    "dnsbl-1.uceprotect.net",
    "dnsbl-2.uceprotect.net",
    "dnsbl-3.uceprotect.net",
    "multi.surbl.org"
]

# File paths
IP_LIST_FILE = "ip_list.txt"
DOMAIN_LIST_FILE = "domain.txt"

# ===================================

def reverse_ip(ip):
    return '.'.join(reversed(ip.split('.')))

# Function to send a webhook notification when an IP or domain is blacklisted
# Set alert Message in this section on message....
def send_webhook_notification(item, blacklists):
    message = {
        "text": f"Warning: {item} is blacklisted in the following blacklists: {', '.join(blacklists)}"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print(f"Notification sent successfully for {item}.")
        else:
            print(f"Failed to send notification for {item}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending notification for {item}: {str(e)}")


def check_blacklist_ip(ip):
    reversed_ip = reverse_ip(ip)
    blacklisted_in = []
    for bl in BLACKLIST_SERVICES:
        try:
            query = f"{reversed_ip}.{bl}"
            dns.resolver.resolve(query, "A")
            blacklisted_in.append(bl)
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.Timeout:
            print(f"Timeout while checking {bl}")
        except dns.resolver.NoNameservers:
            print(f"No nameservers found for {bl}")
    
    return blacklisted_in

def check_blacklist_domain(domain):
    blacklisted_in = []
    for bl in BLACKLIST_SERVICES:
        try:
            query = f"{domain}.{bl}"
            dns.resolver.resolve(query, "A")
            blacklisted_in.append(bl)
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.Timeout:
            print(f"Timeout while checking {bl}")
        except dns.resolver.NoNameservers:
            print(f"No nameservers found for {bl}")
    
    return blacklisted_in

def read_items_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []

def main():
    if len(sys.argv) == 2:
        item = sys.argv[1]

        if item.lower() == 'domain':
            domains = read_items_from_file(DOMAIN_LIST_FILE)
            if not domains:
                print("No domains to check. Please check the file.")
                return
            for domain in domains:
                print(f"\nChecking domain: {domain}")
                blacklisted_in = check_blacklist_domain(domain)
                if blacklisted_in:
                    print(f"Domain {domain} is blacklisted in: {', '.join(blacklisted_in)}")
                    send_webhook_notification(domain, blacklisted_in)
                else:
                    print(f"Domain {domain} is NOT blacklisted in any of the tested blacklists.")
            return

        elif item.lower() == 'ip':
            ip_addresses = read_items_from_file(IP_LIST_FILE)
            if not ip_addresses:
                print("No IP addresses to check. Please check the file.")
                return
            for ip in ip_addresses:
                print(f"\nChecking IP: {ip}")
                blacklisted_in = check_blacklist_ip(ip)
                if blacklisted_in:
                    print(f"IP {ip} is blacklisted in: {', '.join(blacklisted_in)}")
                    send_webhook_notification(ip, blacklisted_in)
                else:
                    print(f"IP {ip} is NOT blacklisted in any of the tested blacklists.")
            return

        else:
            if item.replace(".", "").isdigit():
                print(f"Checking IP: {item}")
                blacklisted_in = check_blacklist_ip(item)
            else:
                print(f"Checking domain: {item}")
                blacklisted_in = check_blacklist_domain(item)

            if blacklisted_in:
                print(f"{item} is blacklisted in: {', '.join(blacklisted_in)}")
                send_webhook_notification(item, blacklisted_in)
            else:
                print(f"{item} is NOT blacklisted in any of the tested blacklists.")
            return

    choice = input("Would you like to check (1) IP or (2) Domain? Enter 1 or 2: Enter 1 or 2: ").strip()

    if choice == "1":
        ip_addresses = read_items_from_file(IP_LIST_FILE)
        if not ip_addresses:
            print("No IP addresses to check. Please check the file.")
            return
        for ip in ip_addresses:
            print(f"\nChecking IP: {ip}")
            blacklisted_in = check_blacklist_ip(ip)
            if blacklisted_in:
                print(f"IP {ip} is blacklisted in: {', '.join(blacklisted_in)}")
                send_webhook_notification(ip, blacklisted_in)
            else:
                print(f"IP {ip} is NOT blacklisted in any of the tested blacklists.")

    elif choice == "2":
        domains = read_items_from_file(DOMAIN_LIST_FILE)
        if not domains:
            print("No domains to check. Please check the file.")
            return
        for domain in domains:
            print(f"\nChecking domain: {domain}")
            blacklisted_in = check_blacklist_domain(domain)
            if blacklisted_in:
                print(f"Domain {domain} is blacklisted in: {', '.join(blacklisted_in)}")
                send_webhook_notification(domain, blacklisted_in)
            else:
                print(f"Domain {domain} is NOT blacklisted in any of the tested blacklists.")

    else:
        print("Invalid choice. Please enter 1 for IP or 2 for Domain.")

if __name__ == "__main__":
    main()
