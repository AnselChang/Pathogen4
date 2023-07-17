from enum import Enum
from data_structures.variable import Variable
from entity_base.entity import Entity
from views.dropdown_view.dropdown_view_config import DropdownConfig
from views.multi_variable_view import MultiVariableView

"""
A view for a dropdown, where one active option out of many
is selected, and clicking on the dropdown reveals the other options
to select from.

This view works with two variables:
    - a string for the active option
    - a list of strings for all the options, including the active one
"""

class DropdownVariable(Enum):
    ACTIVE_OPTION = 0
    ALL_OPTIONS = 1

class DropdownView(Entity, MultiVariableView):

    def __init__(self, parent: Entity,
                 activeOption: Variable[str],
                 allOptions: Variable[list[str]],
                 config: DropdownConfig
                ):
        
        # make sure active option is in list of all options
        assert(activeOption.get() in allOptions.get())
        
        MultiVariableView.__init__(self, {
            DropdownVariable.ACTIVE_OPTION: activeOption,
            DropdownVariable.ALL_OPTIONS: allOptions
        })

        self.config = config

        super().__init__(parent)

