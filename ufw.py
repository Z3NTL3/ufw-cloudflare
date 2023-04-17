import httpx
import subprocess

try:
    # clear first
    subprocess.Popen("ufw reset", shell=True)
    subprocess.Popen("ufw default deny incoming",
                     shell=True)

    with httpx.Client(headers={"Cache-Control": "must-revalidate", "Content-Type": "text/plain"}) as client:
        ipv4s = client.get("https://www.cloudflare.com/ips-v4").text
        ipv6s = client.get("https://www.cloudflare.com/ips-v6").text

        ipv4s = ipv4s.strip().split("\n")
        ipv6s = ipv6s.strip().split("\n")

        for ipv4 in ipv4s:
            subprocess.Popen(
                f"ufw allow proto tcp from {ipv4} comment 'CF IP'", shell=True)
        for ipv6 in ipv6s:
            subprocess.Popen(
                f"ufw allow proto tcp from {ipv6} comment 'CF IP'", shell=True)

        subprocess.Popen("ufw allow ssh",
                         shell=True)
        subprocess.Popen("ufw reload", shell=True)
        subprocess.Popen("ufw enable", shell=True)
except:
    print("Failed")
