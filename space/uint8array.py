from interface import Object
from rpython.rlib.objectmodel import compute_hash
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.rlib import rgc
import numbers
import space

class Uint8Array(Object):
    _immutable_fields_ = ['uint8data', 'length']
    __slots__ = ['uint8data', 'length']
    def __init__(self, uint8data, length):
        self.uint8data = uint8data
        self.length = length

    def repr(self): # Add hexadecimal formatting later..
        return u"<uint8array>"

    #def hash(self):
    #    return compute_hash(self.uint8data)

    #def eq(self, other):
    #    if isinstance(other, Uint8Array):
    #        return self.uint8data == other.uint8data
    #    return False

    def getattr(self, name):
        if name == u'length':
            return numbers.Integer(self.length)
        return Object.getattr(self, name)
        
    def getitem(self, index):
        if not isinstance(index, numbers.Integer):
            raise space.OldError(u"index not an integer")
        if not 0 <= index.value < self.length:
            raise space.OldError(u"index out of range")
        return numbers.Integer(rffi.r_long(self.uint8data[index.value]))

    def setitem(self, index, value):
        if not isinstance(index, numbers.Integer):
            raise space.OldError(u"index not an integer")
        if not 0 <= index.value < self.length:
            raise space.OldError(u"index out of range")
        if not isinstance(value, numbers.Integer):
            raise space.OldError(u"value of incorrect type")
        self.uint8data[index.value] = rffi.r_uchar(value.value)
        return value

    @rgc.must_be_light_finalizer
    def __del__(self):
        lltype.free(self.uint8data, flavor='raw')

def to_uint8array(cstring):
    return Uint8Array(rffi.cast(rffi.UCHARP, rffi.str2charp(cstring)), len(cstring))
