# DuckDNS Update via Cron

This guide shows how to keep your dynamic IP address in sync with [DuckDNS](https://www.duckdns.org/).

1. **Check for `cron` and `curl`**
   ```bash
   ps -ef | grep cr[o]n
   curl --version
   ```
   Install `cron` or `curl` if either command fails.

2. **Create the update script**
   ```bash
   mkdir ~/duckdns
   cd ~/duckdns
   cat <<'SCRIPT' > duck.sh
   echo url="https://www.duckdns.org/update?domains=niorlusxai&token=<YOUR_TOKEN>&ip=" | \
     curl -k -o ~/duckdns/duck.log -K -
   SCRIPT
   chmod 700 duck.sh
   ```

3. **Schedule with `cron`**
   ```bash
   crontab -e
   # Add the line below
   */5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
   ```

4. **Test the setup**
   ```bash
   ~/duckdns/duck.sh
   cat ~/duckdns/duck.log
   ```
   The log should show `OK` if the update succeeded.

Replace the token in the script with your own DuckDNS token if needed:
```bash
curl "https://www.duckdns.org/update?domains=niorlusx&token=YOUR_TOKEN&ip="
```
