from dataclasses import dataclass
from typing import List, Union
import numpy as np

@dataclass
class BinaryMessageData:
    topicId: int
    serverTime: int
    typeInfo: List[int, str]
    value: Union[bool, int, float, str, bytes, bytearray, list]

    def __post_init__(self):
        # Validate the typeInfo and value types
        if not isinstance(self.typeInfo, list) or len(self.typeInfo) != 2:
            raise ValueError("Invalid typeInfo format")

        type_num, type_str = self.typeInfo
        type_info = NetworkTablesTypeInfo.get_network_tables_type_from_type_num(type_num)

        if type_info == NetworkTablesTypeInfo.kBoolean:
            if not isinstance(self.value, bool):
                raise ValueError("Value type mismatch with typeInfo (expected bool)")
        elif type_info == NetworkTablesTypeInfo.kDouble:
            if not is_double(self.value):
                raise ValueError("Value type mismatch with typeInfo (expected double)")
        elif type_info == NetworkTablesTypeInfo.kInteger:
            if not isinstance(self.value, int):
                raise ValueError("Value type mismatch with typeInfo (expected int)")
        elif type_info == NetworkTablesTypeInfo.kString:
            if not isinstance(self.value, str):
                raise ValueError("Value type mismatch with typeInfo (expected string)")
        elif type_info == NetworkTablesTypeInfo.kArrayBuffer:
            if not isinstance(self.value, (bytes, bytearray)):
                raise ValueError("Value type mismatch with typeInfo (expected bytes or bytearray)")
        elif type_info == NetworkTablesTypeInfo.kBooleanArray:
            if not isinstance(self.value, list) or not all(isinstance(x, bool) for x in self.value):
                raise ValueError("Value type mismatch with typeInfo (expected list of bools)")
        elif type_info == NetworkTablesTypeInfo.kDoubleArray:
            if not isinstance(self.value, list) or not all(map(is_double, self.value)):
                raise ValueError("Value type mismatch with typeInfo (expected list of doubles)")
        elif type_info == NetworkTablesTypeInfo.kIntegerArray:
            if not isinstance(self.value, list) or not all(isinstance(x, int) for x in self.value):
                raise ValueError("Value type mismatch with typeInfo (expected list of ints)")
        elif type_info == NetworkTablesTypeInfo.kStringArray:
            if not isinstance(self.value, list) or not all(isinstance(x, str) for x in self.value):
                raise ValueError("Value type mismatch with typeInfo (expected list of strings)")


def is_double(x):
    """
    Check if a given value is a double (floating-point number).
    """
    return isinstance(x, (float, np.floating)) and not isinstance(x, (bool, np.bool_))

class NetworkTablesTypeInfo:
    kBoolean = [0, 'boolean']
    kDouble = [1, 'double']
    kInteger = [2, 'int']
    kString = [4, 'string']
    kArrayBuffer = [3, 'raw']
    kBooleanArray = [16, 'boolean[]']
    kDoubleArray = [17, 'double[]']
    kIntegerArray = [18, 'int[]']
    kStringArray = [20, 'string[]']

    @staticmethod
    def get_network_tables_type_from_object(data):
        """
        Given a value, find the NT type number.
        """
        if isinstance(data, bool):
            return NetworkTablesTypeInfo.kBoolean
        elif isinstance(data, (int, float)):
            if is_double(data):
                return NetworkTablesTypeInfo.kDouble
            return NetworkTablesTypeInfo.kInteger
        elif isinstance(data, str):
            return NetworkTablesTypeInfo.kString
        elif isinstance(data, (bytes, bytearray)):
            return NetworkTablesTypeInfo.kArrayBuffer
        elif isinstance(data, (list, tuple)):
            if len(data) > 0 and len(set(map(type, data))) == 1:
                element_type = type(data[0])
                if element_type == bool:
                    return NetworkTablesTypeInfo.kBooleanArray
                elif element_type in (int, float):
                    if all(map(is_double, data)):
                        return NetworkTablesTypeInfo.kDoubleArray
                    return NetworkTablesTypeInfo.kIntegerArray
                elif element_type == str:
                    return NetworkTablesTypeInfo.kStringArray
        raise ValueError(f"Invalid data for NT: {data}")

    @staticmethod
    def get_network_tables_type_from_type_num(type_num):
        """
        Get the type info from a type number.
        """
        type_info_map = {
            NetworkTablesTypeInfo.kBoolean[0]: NetworkTablesTypeInfo.kBoolean,
            NetworkTablesTypeInfo.kDouble[0]: NetworkTablesTypeInfo.kDouble,
            NetworkTablesTypeInfo.kInteger[0]: NetworkTablesTypeInfo.kInteger,
            NetworkTablesTypeInfo.kString[0]: NetworkTablesTypeInfo.kString,
            NetworkTablesTypeInfo.kArrayBuffer[0]: NetworkTablesTypeInfo.kArrayBuffer,
            NetworkTablesTypeInfo.kBooleanArray[0]: NetworkTablesTypeInfo.kBooleanArray,
            NetworkTablesTypeInfo.kDoubleArray[0]: NetworkTablesTypeInfo.kDoubleArray,
            NetworkTablesTypeInfo.kIntegerArray[0]: NetworkTablesTypeInfo.kIntegerArray,
            NetworkTablesTypeInfo.kStringArray[0]: NetworkTablesTypeInfo.kStringArray,
        }
        if type_num in type_info_map:
            return type_info_map[type_num]
        raise ValueError(f"Invalid type number: {type_num}")

    @staticmethod
    def get_network_tables_type_from_type_string(type_string):
        """
        Get the type info from a type string.
        """
        type_info_map = {
            NetworkTablesTypeInfo.kBoolean[1]: NetworkTablesTypeInfo.kBoolean,
            NetworkTablesTypeInfo.kDouble[1]: NetworkTablesTypeInfo.kDouble,
            NetworkTablesTypeInfo.kInteger[1]: NetworkTablesTypeInfo.kInteger,
            NetworkTablesTypeInfo.kString[1]: NetworkTablesTypeInfo.kString,
            NetworkTablesTypeInfo.kArrayBuffer[1]: NetworkTablesTypeInfo.kArrayBuffer,
            NetworkTablesTypeInfo.kBooleanArray[1]: NetworkTablesTypeInfo.kBooleanArray,
            NetworkTablesTypeInfo.kDoubleArray[1]: NetworkTablesTypeInfo.kDoubleArray,
            NetworkTablesTypeInfo.kIntegerArray[1]: NetworkTablesTypeInfo.kIntegerArray,
            NetworkTablesTypeInfo.kStringArray[1]: NetworkTablesTypeInfo.kStringArray,
        }
        if type_string in type_info_map:
            return type_info_map[type_string]
        raise ValueError(f"Unsupported type string: {type_string}")
