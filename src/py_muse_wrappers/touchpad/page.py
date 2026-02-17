from .component import Component


class Page(Component):
    """
    Page component representing a panel page.

    Contains buttons as subcomponents.
    """

    def render(self):
        """Render page (no-op, pages don't render themselves)."""
        pass
