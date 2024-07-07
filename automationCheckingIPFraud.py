import pandas as pd
import requests

# API keys
securitytrails_api_key = "O1FBgp8FprV6TFO5N7npItjJ2C7SOrzJ"
ipinfo_token = "e7eb5646acf009"

def securitytrails_lookup(ip):
    url = f"https://api.securitytrails.com/v1/ips/{ip}/whois"
    headers = {
        "APIKEY": securitytrails_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        hostname = data.get("current_dns", {}).get("hostname", "N/A")
        return hostname
    else:
        return "Error"

def ipinfo_lookup(ip):
    url = f"https://ipinfo.io/{ip}/json?token={ipinfo_token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        domains = data.get("domains", {}).get("domains", [])
        if domains:
            return ", ".join(domains)
        else:
            return "N/A"
    else:
        return "Error"

# readfile function
file_path = "test1.xlsx"
df = pd.read_excel(file_path)

# Inisialisasi kolom baru
df['SecurityTrails_Domain'] = ""
df['IPinfo_Domains'] = ""

# lookup Dest
for index, row in df.iterrows():
    ip = row['destipv4addr']
    df.at[index, 'SecurityTrails_Domain'] = securitytrails_lookup(ip)
    df.at[index, 'IPinfo_Domains'] = ipinfo_lookup(ip)

output_file_path = "path_to_output_excel_file.xlsx"
df.to_excel(output_file_path, index=False)
