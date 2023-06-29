from __future__ import annotations
from typing import TYPE_CHECKING

from utility.misc_functions import getEnumFromName
if TYPE_CHECKING:
    from adapter.path_adapter import PathAdapter, PathAttributeID
    from root_container.panel_container.command_block.parameter_state import ParameterState


class CodeGenerationService:

    def __init__(self,
                codeTemplate: str,
                adapter: PathAdapter,
                parameters: ParameterState,
                testingOnly: bool = False
    ):
        
        self.codeTemplate = codeTemplate
        self.adapter = adapter
        self.parameters = parameters
        self.testingOnly = testingOnly

    # given a variableName, presumbly found under $variableName$,
    # search for a match in both adapter and parameters
    def getVariableValue(self, variableName: str) -> str | None:
        
        matchingEnum = getEnumFromName(PathAttributeID, variableName)
        if matchingEnum is not None:
            # check if it's in adapter
            value = self.adapter.getValue(matchingEnum)
            if value is not None:
                return str(value)

        # check if it's in parameters
        value = self.parameters.getValueByName(variableName)
        if value is not None:
            return str(value)
        
        # if not found, return None
        return None
    
    def getVariableValueDummy(self, variableName: str) -> str | None:
        if variableName == "ONE":
            return "1"
        elif variableName == "TWO":
            return "2"
        elif variableName == "THREE":
            return "3"
        else:
            return None

    # find all instances of $VARIABLE$ and attempt to replace with values
    def generateCode(self) -> str:

        code = self.codeTemplate
        # find all instances of $VARIABLE$
        start = 0
        while True:
            start = code.find('$', start)
            if start == -1:
                break
            end = code.find('$', start + 1)
            if end == -1:
                break
            
            variableName = code[start + 1:end]

            if self.testingOnly:
                variableValue = self.getVariableValueDummy(variableName)
            else:
                variableValue = self.getVariableValue(variableName)
            print(variableName, variableValue)
            
            if variableValue is not None:
                code = code[:start] + variableValue + code[end + 1:]
            else:
                # if variableValue is None, we try the next substring starting with $,
                # which was the previous end $
                start = end

        return code
    