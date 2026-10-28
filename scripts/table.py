import json, sys, csv, re, datetime as dt
rows=[json.loads(l) for l in open(sys.argv[1])]
for r in rows: r['n']=int(re.match(r'Flooding expt (\d+)', r['file']).group(1))
rows.sort(key=lambda r:r['n'])
out=csv.writer(open(sys.argv[2],'w',newline=''))
hdr=['expt','file','label_in_name','original_zen_name','start_local_CST','stop_local_CST','frames','duration_s','median_interval_s','size_MB','focus_pos_MTBFocus','display_low','display_high']
out.writerow(hdr)
import xml.etree.ElementTree as ET
for r in rows:
    start=dt.datetime.fromisoformat(r['created'][:26]+r['created'][-6:])
    stop=dt.datetime.fromisoformat(r['timeline'][0][0][:26]+'+00:00').astimezone(start.tzinfo)
    lab=re.sub(r'^Flooding expt \d+\s*','',r['file']).replace('10012020.czi','').strip() or '(none)'
    x=open(f"{sys.argv[3]}/"+re.sub(r'\s+','_',r['file'][:-4])+'.xml').read()
    md=ET.fromstring(x).find('Metadata')
    foc=[pc.findtext('Position') for pc in md.iter('ParameterCollection') if pc.get('Id')=='MTBFocus'][0]
    row=[r['n'],r['file'],lab,r['orig_name'].split('\\')[-1],start.strftime('%H:%M:%S'),stop.strftime('%H:%M:%S'),r['SizeT'],round(r['duration_s'],1),round(r['dt_med'],3),round(r['bytes']/1e6,1),foc,round(float(r['disp_low'])*65535),round(float(r['disp_high'])*65535)]
    out.writerow(row); print(row)
