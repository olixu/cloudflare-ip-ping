# cloudflare-ip-ping
Cloudflare provides a CDN service which can speed up the websites. While using the free plan, you could not choose the nodes of the CDN. However, The cloudflare partner project allows users to use cname to get their websites into the CDN, which means users can choose whichever nodes they like.

There are some situations that you only want to speed up your websites at your location. I will tell you how to use Python to choose the the ip that suits you best.

## Principle
Cloudflare has a ip list of their CDN, which can be obtained at [here](https://www.cloudflare.com/ips/). The method that i use is very simple:

1. Ping the IPs and get the latency and loss. 
2. Choose the best IP.
3. Use Cloudflare Partner Project to cname your domain to the chosen ip.

## Usage

```bash 
python pingip.py
```

You will get a log file in your current directory.
