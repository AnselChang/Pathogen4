from adapter.bezier_adapter import BezierAdapterState
from adapter.path_adapter import AdapterState, PathAdapter
from command_creation.command_type import CommandType
from common.image_manager import ImageID
from entity_base.image.image_state import ImageState

class NullAdapterState(AdapterState):
    def _deserialize(self) -> 'PathAdapter':
        return NullAdapter([ImageState.deserialize(state) for state in self.iconImageStates])

class NullAdapter(PathAdapter):
    def __init__(self, _ = None):
        image = ImageState(0, ImageID.CUSTOM)
        super().__init__(CommandType.CUSTOM, image)
        
    def _serialize(self) -> NullAdapterState:
        return NullAdapterState(self.type, self.iconImageStates)