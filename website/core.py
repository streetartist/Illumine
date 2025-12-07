from illumine.theme_manager import ThemeManager

class SiteManager:
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager

    def render_page(self, title: str, content: str):
        return self.theme_manager.render("page.html", title=title, content=content)
