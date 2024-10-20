# Blacklist Checker Script
This Python script checks if a list of IP addresses or domains is blacklisted by various DNSBL (Domain Name System Blacklists). It can either:

  * Check a single IP or domain provided via the command-line.
  * Check all IPs from a file (ip_list.txt).
  * Check all domains from a file (domain.txt).
  * The script also sends a notification to a webhook (e.g., Slack, Discord, etc.) when an IP or domain is found in any blacklist.
## Installing Required Libraries
To install the required libraries, run:
```
pip install dnspython requests
```

## Files
  * ip_list.txt: File containing a list of IP addresses to check, one per line.
  * domain.txt: File containing a list of domains to check, one per line.
  * script.py: The main Python script for checking blacklists.

## Configuration
Make sure to replace the webhook_url in the script with the actual webhook URL where you want to send notifications:
```
# Webhook URL (replace this with your actual webhook URL)
webhook_url = "https://example.com/webhook"
```

When an IP or domain is found to be blacklisted, a POST request is sent to the configured webhook URL with the following JSON structure:
```
{
  "text": "Warning: example.com is blacklisted in the following blacklists: bl.spamcop.net, sbl.spamhaus.org"
}
```
If no IP or domain is blacklisted, no webhook notification is sent.

## Usage
The script can be run in three different modes depending on the input:

### 1. Check a single IP or domain
You can pass an IP address or domain as an argument. The script will check if that single IP or domain is blacklisted.
```
python script.py 192.0.2.1
```
```
python script.py example.com
```
### 2. Check all IPs in ip_list.txt
You can check all IPs listed in ip_list.txt by running the following command:
```
python script.py ip
```
### 3. Check all domains in domain.txt
You can check all domains listed in domain.txt by running the following command:
```
python script.py domain
```
### 4. Interactive mode (No argument)
If no arguments are provided, the script will ask whether you want to check IPs or domains:
```
python script.py
```
You will be prompted with:
```
Would you like to check (1) IP or (2) Domain? Enter 1 or 2:
```
Choose 1 to check IPs from ip_list.txt or 2 to check domains from domain.txt.

## Example Files
### ip_list.txt
```
192.0.2.1
192.1.100.2
192.2.113.5
```
### domain.txt
```
example.com
testdomain.org
sub.example.net
```
## Contributing
Feel free to open an issue or submit a pull request if you have any improvements, suggestions, or bug reports. Contributions are always welcome!

### Contact
For any inquiries or questions, you can reach me on [Telegram](https://t.me/Ali_n7723)
