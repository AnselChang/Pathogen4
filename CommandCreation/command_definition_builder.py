from CommandCreation.command_definition import CommandDefinition

"""
Used to store and update the temporary state while the command is being designed by the user.
Handles stuff like adding each individual widget at a time, renaming, etc.
When the user is finished, instantiates an immutable CommandDefinition
"""

class CommandDefinitionBuilder:

    def build(self) -> CommandDefinition:
        pass