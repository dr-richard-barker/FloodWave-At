import sys, os, json, czifile, numpy as np, xml.etree.ElementTree as ET
rows=[]
for src in sys.argv[1:]:
    with czifile.CziFile(src) as c:
        md = ET.fromstring(c.metadata()).find('Metadata')
        g = lambda p: (md.findtext(p) or '').strip()
        img = 'Information/Image/'
        ch = md.find(img+'Dimensions/Channels/Channel')
        row = dict(file=os.path.basename(src), bytes=os.path.getsize(src),
          orig_name=g('Experiment/ImageName') or next((e.text for e in md.iter('ImageName')), ''),
          created=g('Information/Document/CreationDate'),
          acq_utc=g(img+'AcquisitionDateAndTime'),
          SizeX=g(img+'SizeX'), SizeY=g(img+'SizeY'), SizeT=g(img+'SizeT'), SizeC=g(img+'SizeC'),
          SizeZ=g(img+'SizeZ'), SizeS=g(img+'SizeS'), SizeM=g(img+'SizeM'),
          interval_s=g(img+'Dimensions/T/Positions/Interval/Increment'),
          channel=ch.get('Name'), exc=ch.findtext('ExcitationWavelength'), em=ch.findtext('EmissionWavelength'),
          reflector=ch.findtext('Reflector'), exposure_ns=ch.findtext('ExposureTime'),
          binning=ch.findtext('DetectorSettings/Binning'), intensity=ch.findtext('LightSourcesSettings/LightSourceSettings/Intensity'),
          zoom=g(img+'MicroscopeSettings/ZoomSettings/Magnification'),
          objective=md.find('Information/Instrument/Objectives/Objective').get('Name'),
          microscope=md.find('Information/Instrument/Microscopes/Microscope').get('Name'),
          px_m=g("Scaling/Items/Distance[@Id='X']/Value"),
          disp_low=md.findtext('DisplaySetting/Channels/Channel/Low'), disp_high=md.findtext('DisplaySetting/Channels/Channel/High'),
          palette=md.findtext('.//PaletteName'))
        stops = [(e.findtext('Time'), e.findtext('EventInformation/ExecutionInformation/Type'), e.find('Bounds').attrib if e.find('Bounds') is not None else None) for e in md.iter('TimelineElement')]
        row['timeline']=stops
        att = {}
        for a in c.attachments():
            name = a.attachment_entry.name
            try: d = a.data()
            except Exception as ex: d = f'ERR {ex}'
            att[name]=d
        row['attachments']=list(att)
        ts = att.get('TimeStamps')
        if isinstance(ts, np.ndarray) or isinstance(ts,(list,tuple)):
            ts=np.asarray(ts, float); row['ts_n']=len(ts); row['ts_first']=ts[0]; row['ts_last']=ts[-1]
            dt=np.diff(ts); row['dt_med']=float(np.median(dt)); row['dt_min']=float(dt.min()); row['dt_max']=float(dt.max())
            row['duration_s']=float(ts[-1]-ts[0])
        ev = att.get('EventList')
        row['events']=repr(ev)[:600] if ev is not None else None
        # check subblock T indices continuity
        tidx = sorted(sb.start[sb.axes.index('T')] for sb in c.filtered_subblock_directory)
        row['t_range']=(tidx[0], tidx[-1], len(tidx), len(set(tidx)))
        rows.append(row)
        print(json.dumps(row, default=str))
