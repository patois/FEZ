import os, sys
from fezpak import *

FILE_EXTENSION = ".file"

def pak_extract(src, target):
    failures = 0

    if os.path.exists(target):
        print "\n[!] Error: target directory exists"
        return

    fp = FEZPak()
    count = fp.import_pak(src)
    if count != fp.get_resource_count():
        print "\n[!] Error: could not read all resources"
        return
    
    for i in xrange(fp.get_resource_count()):
        res = fp.get_resource(i)
        if res is not None:
            fileName, data = res
            res = None
            try:
                p = os.path.join(tgt, fileName)
                if not os.path.exists(os.path.dirname(p)):
                    os.makedirs(os.path.dirname(p))
                print "%s -> %s" % (fileName, p + FILE_EXTENSION)
                f = open(p + FILE_EXTENSION, "wb")
                f.write(data)
                f.close()
            except:
                failures += 1
    if failures:
        print "\n[!] Error: could not extract all resources"
    return

def pak_build(src, target):
    failures = 0

    if not os.path.exists(src):
        print "\n[!] Error: source directory does not exist"
        return

    if os.path.exists(target):
        print "\n[!] Error: target pak file exists"
        return

    fp = FEZPak()
    for root, dirs, files in os.walk(src):
        for name in files:
            importas, ext = os.path.splitext(os.path.join(root[len(src)+1:],name))
            infile = os.path.join(root, name)
            print "%s -> %s" % (infile, importas)
            fp.import_resource_from_file(infile, importas)
    fp.export_pak(target)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage:\n\n%s <mode> <source> <target>" % os.path.basename(sys.argv[0])
        print "\tmodes:\n\tx - extract source=pak_file target=path\n\tb - build source=path target=pak_file"
        sys.exit(0)
        
    mode = sys.argv[1]
    src = sys.argv[2]
    tgt = sys.argv[3]
    if mode == "x":
        pak_extract(src, tgt)
    elif mode == "b":
        pak_build(src, tgt)

