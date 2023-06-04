from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget
from textual.geometry import Size


class Hello(Widget):
    """Display a greeting."""

    def render(self) -> RenderResult:
        return "Hello, [b]World[/b]!"

    # def get_content_width(self, container: Size, viewport: Size) -> int:
    #     """Force content width size."""
    #     return 10

    # def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
    #     """Force content width size."""
    #     return 5


class CustomApp(App):
    CSS_PATH = "test.css"

    def compose(self) -> ComposeResult:
        yield Hello()


if __name__ == "__main__":
    app = CustomApp()
    app.run()
