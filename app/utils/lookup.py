
class Lookup():
  """
    abstract lookup class
  """

  def __init__(self, type):
    self.type = type

  @abstractmethod
  def get(self, value, default):
    raise NotImplementedError

# this will keep track of all the lookup data classes
data_lookup_list = dict()

def register_lookup(lookupObject : Lookup)->None:
  """
    add the lookup class instance to the lookup registry list
  """
  data_lookup_list[lookupObject.type] = lookupObject

def get(lookup_type, key):
  """
    return the lookup value associated with the `key` for the lookup 
    data type `typev`
  """
  if lookup_type in data_lookup_list:
    return data_lookup_list[lookup_type].get(key)
  return None