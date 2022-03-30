# crtsh-client

Checks the crt.sh page every day and records when a new certificate is created, is about to expire according to the variable "daysBeforeExpire" or has already expired.

## How it works

Create a config file name crtsh.conf with this information in the root directory. (there is a example file in the repository)

```
[Config]
domains: example.com, example2.com
daysBeforeExpire = 10

```

## Logging
The script will log all the events to /var/log/syslog and stdout as a syslog format.
