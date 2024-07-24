# Import and register all page-specific callbacks
def setup_pages(app):
    from . import home, page1, page2

    home.register_callbacks(app)
