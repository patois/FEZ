import struct

class FEZPak:
    """
    this class handles FEZ .pak files
    - pak files are assumed to be well formed
      there is no extended error checking
    - tested under Windows on Windows version of FEZ,
      might not work on other OSes
    """

    def __init__(self):
        self.resources = []

    def _read_int(self, f):
        return struct.unpack("I", f.read(4))[0]

    def _write_int(self, f, value):
        return f.write(struct.pack("I", value))

    def _read_byte(self, f):
        return struct.unpack("B", f.read(1))[0]

    def _write_byte(self, f, value):
        return f.write(struct.pack("B", value))

    def _read_buf(self, f, size):
        return f.read(size)

    def _write_buf(self, f, buf):
        return f.write(buf)

    def _seek(self, f, offs, whence = 0):
        return f.seek(offs, whence)

    def _ftell(self, f):
        return f.tell() 

    def import_pak(self, path):
        f = None
        count = 0
        try:
            f = open(path, "rb")
            count = self._read_int(f)
            for i in xrange(count):
                temp = self._read_byte(f)
                fileName = self._read_buf(f, temp)
                size = self._read_int(f)
                buf = self._read_buf(f, size)
                self.add_resource(fileName, buf)
            f.close()
            f = None
        except IOError:
            if f is not None:
                f.close()
        return count

    def export_pak(self, path):
        f = None
        try:
            f = open(path, "wb")
            count = self.get_resource_count()
            self._write_int(f, count)
            for i in xrange(count):
                res = self.get_resource(i)
                if res is not None:
                    fileName, data = res
                    flen = len(fileName)
                    size = len(data)
                    self._write_byte(f, flen)
                    self._write_buf(f, fileName)
                    self._write_int(f, size)
                    self._write_buf(f, data)
            f.close()
        except IOError:
            if f is not None:
                f.close()
            return False
        return True

    def get_resource_count(self):
        return len(self.resources)

    def add_resource(self, name, data):
        self.resources.append((name, data))

    def get_resource(self, idx):
        result = None
        if idx <= self.get_resource_count():
            result = self.resources[idx]
        return result    

    def import_resource_from_file(self, s, import_as):
        l = len(import_as)
        if not l or l > 255:
            return False
        f = None
        try:
            f = open(s, "rb")
            buf = f.read()
            f.close()
        except:
            if f is not None:
                f.close()
            return False

        return self.add_resource(import_as, buf)     

    def del_resource(self, idx):
        self.resources.pop(idx)

    def clear_resources(self):
        self.resources = []      
        
