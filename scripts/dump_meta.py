import sys, os, czifile
src = sys.argv[1]; out = sys.argv[2]
with czifile.CziFile(src) as c:
    xml = c.metadata()
    print(os.path.basename(src), c.shape, c.axes, c.dtype, 'subblocks', len(c.filtered_subblock_directory))
    with open(out, 'w') as f: f.write(xml)
