import os.path
import struct


class StcBinaryReader:
    def __init__(self, _buf):
        self.buf = _buf

    def read_bytes(self):
        output = self.buf.read(1)

        return output

    def read_short(self):
        output = struct.unpack("h", self.buf.read(2))[0]

        return output

    def read_ushort(self):
        output = struct.unpack("H", self.buf.read(2))[0]

        return output

    def read_int(self):
        output = struct.unpack("i", self.buf.read(4))[0]

        return output

    def read_uint(self):
        output = struct.unpack("I", self.buf.read(4))[0]

        return output

    def read_long(self):
        output = struct.unpack("l", self.buf.read(8))[0]

        return output

    def read_ulong(self):
        output = struct.unpack("L", self.buf.read(8))[0]

        return output

    def read_single(self):
        output = struct.unpack("f", self.buf.read(4))[0]

        return output

    def read_double(self):
        output = struct.unpack("d", self.buf.read(8))[0]

        return output

    def read_string(self):
        self.buf.seek(1, 1)        # param = offset + 1 , SEEK_CUR
        length = self.read_short()
        output = struct.unpack("s", self.buf.read(length))[0]

        return output

    def stc_seek(self, _offset, _whence=0):
        if type(_whence) != "int":
            if _whence == "SEEK_SET":
                whence = 0
            elif _whence == "SEEK_CUR":
                whence = 1
            elif _whence == "SEEK_END":
                whence = 2
            else:
                whence = 0
                exit()
        else:
            whence = _whence

        self.buf.seek(_offset, whence)


class StcUtil:
    @staticmethod
    def _parse_stc(self, _src, _start_offset=0):
        output = list()

        with open(_src, "rb") as fp:
            reader = StcBinaryReader(fp)
            reader.read_ushort()

            row = reader.read_short()
            col = int.from_bytes(reader.read_bytes(), byteorder="little")

            col_type = list()
            if row > 0 and col > 0:
                for i in range(0, col):
                    size = int.from_bytes(reader.read_bytes(), byteorder="little")
                    if size == 1:
                        col_type.append("byte")
                    elif size == 5:
                        col_type.append("int")
                    elif size == 8:
                        col_type.append("long")
                    elif size == 9:
                        col_type.append("single")
                    elif size == 11:
                        col_type.append("string")
                    else:
                        col_type.append("unknown(%d)" % size)

            if _start_offset <= 0:
                reader.read_int()
                _start_offset = reader.read_int()
            reader.stc_seek(_start_offset)

            col_names = list()

            if os.path.isfile("STCFormat/"+ ".format"):
                pass
            else:
                print("format not exitst >> %s")

            try:
                for r in range(0, row):
                    pass
            except Exception as ex:
                print("ERROR! >>" + ex)
