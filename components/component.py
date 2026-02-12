"""
Base Component abstraction for hierarchical UI components.

Components have:
- State (dict)
- Subcomponents (hierarchical structure)
- render() method (renders self and subcomponents)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Component(ABC):
    """
    Abstract base class for UI components.

    All components (Panel, Page, Button) inherit from this.
    Provides state management, hierarchical structure, and rendering.
    """

    def __init__(self, name: str):
        """
        Initialize component.

        Args:
            name: Component identifier
        """
        self.name = name
        self.state: Dict[str, Any] = {}
        self._subcomponents: List['Component'] = []

    @property
    def subcomponents(self) -> List['Component']:
        """Get subcomponents list"""
        return self._subcomponents

    def add_subcomponent(self, component: 'Component'):
        """
        Add a subcomponent to the list.

        Args:
            component: Component instance
        """
        self._subcomponents.append(component)

    @abstractmethod
    def render(self):
        """
        Render this component.

        Override this to implement component-specific rendering logic.
        """
        pass

    def render_all(self):
        """
        Render this component and recursively render all subcomponents.
        """
        self.render()
        for subcomponent in self._subcomponents:
            subcomponent.render_all()

    def export_state(self) -> Dict[str, Any]:
        """
        Export state from this component and all subcomponents.

        Returns:
            Dictionary with state hierarchy (not component structure, just state data)
        """
        exported = {
            "name": self.name,
            "state": self.state.copy(),
            "subcomponents": []
        }

        for subcomponent in self._subcomponents:
            exported["subcomponents"].append(subcomponent.export_state())

        return exported

    def import_state(self, state_dict: Dict[str, Any]):
        """
        Import state into this component and all subcomponents.

        Args:
            state_dict: Dictionary with state hierarchy
        """
        if "state" in state_dict:
            self.state.update(state_dict["state"])

        if "subcomponents" in state_dict:
            sub_states = state_dict["subcomponents"]
            # Match subcomponents by index (order matters)
            for i, sub_state in enumerate(sub_states):
                if i < len(self._subcomponents):
                    self._subcomponents[i].import_state(sub_state)


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', subcomponents={len(self._subcomponents)})"

    def __bool__(self) -> bool:
        """Components are always truthy (even if they have no subcomponents)"""
        return True

    def __len__(self) -> int:
        """Return number of subcomponents"""
        return len(self._subcomponents)

    def __iter__(self):
        """Iterate over subcomponents"""
        return iter(self._subcomponents)

    def __getitem__(self, index: int) -> 'Component':
        """Get subcomponent by index"""
        return self._subcomponents[index]
