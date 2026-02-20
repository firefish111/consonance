import numpy
import json
import types
import logging

# to ensure that it's packed f32 binary.
def pack_to_float_array(generator):
  arr = numpy.array([*generator], dtype=numpy.float32)
  return arr.tobytes()

# to convert any data into network-appropriate data
def serialise(data):
  if isinstance(data, dict):
    return json.dumps(data)

  if isinstance(data, types.GeneratorType):
    return pack_to_float_array(data)

  return data

# to convert ticket. really done to put all the serialisation methods in one place
to_ticket = json.loads
