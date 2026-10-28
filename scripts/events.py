import sys, os, czifile
for src in sys.argv[1:]:
    with czifile.CziFile(src) as c:
        for a in c.attachments():
            if a.attachment_entry.name=='EventList':
                for ev in a.data():
                    print(os.path.basename(src), '|', ev.time, ev.event_type, ev.EV_TYPE.get(ev.event_type) if hasattr(ev,'EV_TYPE') else '', '|', repr(ev.description))
