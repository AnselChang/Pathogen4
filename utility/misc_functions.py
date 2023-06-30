from enum import Enum

# Find an enum value based on the name of the num value
def getEnumFromName(enumType: type[Enum], name):
    for enum in enumType:
        if enum.name == name:
            return enum
    return None