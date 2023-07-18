from data_structures.observer import Observer
from data_structures.variable import Variable

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

This class exposes some sort of getValue() function for subclasses
implementing this, and a onExternalValueChange() to be implemented by
subclasses, which would be called when something externally modifies the variable
value, and the view needs to update to reflect that.
This callback will be setup through subscribing to the Variable's changes.
"""

class View(Observer):
    pass