from mcp.server.fastmcp import FastMCP


class EditorMCP(FastMCP):
    def __init__(self):
        super().__init__("EditorMCP")
        self._editor_name = "Unknown Editor"
        self.add_tool(self.get_editor_name)
        self.add_tool(self.set_editor_name)

    def set_editor_name(self, name: str):
        """Sets the name of the editor."""
        self._editor_name = name

    def get_editor_name(self) -> str:
        """Returns the name of the editor."""
        return self._editor_name


def create_editor_mcp() -> EditorMCP:
    return EditorMCP()
