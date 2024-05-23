from enum import Enum

class NetworkTableEntryType(Enum):
    """
    Represents the different types of entries that can be stored in a Network Table.

    Attributes:
        VALUE (int): A regular key-value entry.
        RAW (int): A raw data entry, used to store binary data.
        RPC (int): A remote procedure call entry, used for remote function invocation.
    """
    VALUE = 0
    RAW = 1
    RPC = 2

class NetworkTableUpdateType(Enum):
    """
    Represents the different types of updates that can occur in a Network Table.

    Attributes:
        ENTRY_ASSIGNMENT (int): The assignment of a new entry in the table.
        ENTRY_UPDATE (int): An update to an existing entry in the table.
        ENTRY_DELETE (int): The deletion of an entry from the table.
        TABLE_DELETE (int): The deletion of an entire table.
    """
    ENTRY_ASSIGNMENT = 0
    ENTRY_UPDATE = 1
    ENTRY_DELETE = 2
    TABLE_DELETE = 3

class NetworkTablePermissionType(Enum):
    """
    Represents the different permission levels for Network Table entries.

    Attributes:
        NONE (int): No permission.
        READ (int): Read permission.
        WRITE (int): Write permission.
        READ_WRITE (int): Both read and write permissions.
    """
    NONE = 0
    READ = 1
    WRITE = 2
    READ_WRITE = 3

class NetworkTablesType(Enum):
    """
    Represents the different data types supported by Network Tables.

    Attributes:
        BOOLEAN (str): Boolean data type.
        DOUBLE (str): Double-precision floating-point data type.
        INTEGER (str): Integer data type.
        STRING (str): String data type.
        BOOLEAN_ARRAY (str): Array of boolean values.
        DOUBLE_ARRAY (str): Array of double-precision floating-point values.
        INTEGER_ARRAY (str): Array of integer values.
        STRING_ARRAY (str): Array of string values.
        RAW (str): Raw binary data type.
        BYTE_ARRAY (str): Array of byte values.
        FLOAT (str): Single-precision floating-point data type.
        FLOAT_ARRAY (str): Array of single-precision floating-point values.
    """
    BOOLEAN = 'boolean'
    DOUBLE = 'double'
    INTEGER = 'integer'
    STRING = 'string'
    BOOLEAN_ARRAY = 'boolean[]'
    DOUBLE_ARRAY = 'double[]'
    INTEGER_ARRAY = 'integer[]'
    STRING_ARRAY = 'string[]'
    RAW = 'raw'
    BYTE_ARRAY = 'byte[]'
    FLOAT = 'float'
    FLOAT_ARRAY = 'float[]'