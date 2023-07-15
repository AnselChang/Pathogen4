"""
The base view that holds a single Variable as state. This is part
of the MVC design pattern, using the Variable as a single source
of truth between the model and the view. However, the view doesn't
construct the variable, but rather, the variable (presumably owned
by the model) is injected into the view.

Possible subclasses involve a text box, a dropdown, checkbox, etc,
anything that displays and modifies a single value. Through this design,
subclasses have unlimited flexibility on how they want to display the
variable.

This class exposes a getValue() functino for subclasses
implementing this, and a onExternalValueChange() to be implemented by
subclasses, which would be called when something externally modifies the variable
value, and the view needs to update to reflect that.
This callback will be setup through subscribing to the Variable's changes.
"""

from data_structures.observer import Observer
from data_structures.variable import Variable


class View(Observer):

    def __init__(self, variable: Variable):

        super().__init__()
        
        self.variable = variable
        self.variable.subscribe(self, onNotify = self.onExternalValueChange)

    # get the current value of the variable
    def getValue(self):
        return self.variable.get()
    
    # set a new value for the variable
    # note that anything subscribed to the variable (ie. model)
    # should be notified of the change
    def setValue(self, value):
        self.variable.set(value)

    # called when the variable is changed externally
    def onExternalValueChange(self):
        pass