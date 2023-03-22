from aenum import Enum

class MCVersion(Enum, init='int str'):
   JE = (0, "JE")
   BE = (1, "BE")