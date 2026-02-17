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


    @abstractmethod
    def render(self):
        """
        Render this component.

        Override this to implement component-specific rendering logic.
        """
        pass

   