"""poking.py goal action module


"""
#print("module {0}".format(__name__))

import time
import struct

from collections import deque
try:
    from itertools import izip
except ImportError: # python3
    izip = zip
import inspect



from .globaling import *
from .odicting import odict

from . import aiding
from . import excepting
from . import registering

from . import storing
from . import acting

from .consoling import getConsole
console = getConsole()

class Poke(acting.Actor):
    """Poke Class to put values into explicit shares

    """
    Registry = odict()

    def action(self, share, data, **kw):
        """Put data into share """
        console.profuse("Put {0} into {1}\n".format( data, share.name))

        share.update(data)


class DirectPoke(Poke):
    """Direct Poke Class to put direct data values into destination share

    """
    def action(self, data, destination, **kw):
        """ Put data into share
            parameters:
              data = data to copy from
              destination = share to copy to
        """
        console.profuse("Put {0} into {1}\n".format( data, destination.name))

        destination.update(data)


class IndirectPoke(Poke):
    """Indirect Poke Class to copy values from one share to another
       based on source and destination field lists

    """
    def action(self, source, sourceFields, destination, destinationFields, **kw):
        """ Copy sourceFields in source to destinationFields in destination

            copy fields in order according to field lists
              field list order is significant
                 a field of same name in source and destination will
                 not be copied to each other unless appear in same place
                 in both field lists

            parameters:
                source = share to copy from
                sourceFields = list of fields to copy from
                destination = share to copy to
                destinationFields = list of fields to copy to

        """
        console.profuse("Copy {0} in {1} into {2} in {3}\n".format(
            sourceFields, source.name, destinationFields, destination.name))

        data = odict()

        for df, sf in izip(destinationFields, sourceFields):
            data[df] = source[sf]

        destination.update(data) #updates time stamp as well

        console.profuse("Copied {0} into {1}\n".format(
                    data, destination.name))
        return None

class DirectInc(Poke):
    """Direct Poke Class to put direct data values into destination share

    """
    def action(self, destination, data, **kw):
        """ Increment destinationFields in destination by values in data

            if only one field then single increment
            if multiple fields then vector increment

            parameters:
                destination = share to increment
                data = dict of field values to increment by
        """
        try:
            dstData = odict()
            for field in data:
                dstData[field] = destination[field] + data[field]
            destination.update(dstData) #update so time stamp updated, use dict
        except TypeError as ex: #in case value is not a number
            console.terse("Error in Inc: {0}\n".format(ex))
        else:
            console.profuse("Inc {0} in {1} by {2} to {3}\n".format(
                data.keys(), destination.name, data.values(), dstData.values()))

class IndirectInc(Poke):
    """Indirect Poke Class to copy values from one share to another
       based on source and destination field lists

    """
    def action(self, destination, destinationFields, source, sourceFields, **kw):
        """ Increment destinationFields in destination by sourceFields in source
            parameters:
                destination = share to increment
                destinationField = field in share to increment
                source = share with value to increment by
                sourceField = field in share with value to increment by

        """
        try:
            data = odict()
            for dstField, srcField in izip(destinationFields, sourceFields):
                data[dstField] = destination[dstField] + source[srcField]
            destination.update(data) #update so time stamp updated, use dict
        except TypeError as ex:
            console.terse("Error in Inc: {0}\n".format(ex1))
        else:
            console.profuse("Inc {0} in {1} from {2} in {3} to {4}\n".format(
                destinationFields, destination.name, sourceFields, source.name, data.values))

def Test():
    """Module Common self test

    """
    pass


if __name__ == "__main__":
    test()

