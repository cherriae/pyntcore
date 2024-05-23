from enum import Enum

class NetworkTablesType(Enum):
    BOOLEAN = 'boolean'
    DOUBLE = 'double'
    INTEGER = 'integer'
    STRING = 'string'
    BOOLEAN_ARRAY = 'boolean[]'
    DOUBLE_ARRAY = 'double[]'
    INTEGER_ARRAY = 'integer[]'
    STRING_ARRAY = 'string[]'