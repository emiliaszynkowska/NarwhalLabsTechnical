# Incident note: inbox-api outage during Aurora failover

**When:** last night, 02:14 to about 02:22 (UTC).

**What we saw.** Aurora ran a failover that took the writer offline for
roughly 40 seconds. In that window the inbox-api pods went into
CrashLoopBackOff. They did not recover when the database came back at
02:15. Instead they kept restarting in a storm, and the service stayed
down for about 8 minutes in total, well past the point where the
database was healthy again.

**What we expected.** A 40-second database blip should have meant a short
spell of shed traffic and then a clean recovery. A brief degradation, not
an 8-minute outage with pods thrashing.

**Ask.** Work out why a short database blip took the whole service down and
kept it down. Fix what you can in `app.py` and `deployment.yaml`, and write
up what else you would change and why.
