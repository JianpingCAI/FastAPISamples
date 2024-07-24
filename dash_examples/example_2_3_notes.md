## Tutorial: Creating a Multi-Page Dash Application with Data Sharing and Callbacks

In this tutorial, we'll explore how to build a multi-page Dash application that shares data between pages and manages callbacks efficiently. This approach is ideal for creating scalable and maintainable applications.

### Overview

Our application will consist of three main parts:
1. **Home Page**: Users can enter data that will be shared across other pages.
2. **Page 1 and Page 2**: Display the data entered on the Home Page and allow further interactions.

We will also implement a navigation system to move between pages without losing state.

### Project Structure

Organize your project into the following structure:

```
multi-page-dash-app/
├── app.py
├── pages/
│   ├── __init__.py
│   ├── home.py
│   ├── page1.py
│   └── page2.py
```

### Step-by-Step Guide

#### Step 1: Setup the Dash App

**`app.py`**:
This file initializes the Dash app and includes the layout and main callbacks.

```python
import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
from pages import setup_pages

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="shared-data", storage_type="session"),
        html.Div(id="page-content")
    ]
)

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/page1":
        from pages.page1 import layout as page1_layout
        return page1_layout
    elif pathname == "/page2":
        from pages.page2 import layout as page2_layout
        return page2_layout
    from pages.home import layout as home_layout
    return home_layout

setup_pages(app)

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### Step 2: Define the Pages

Each page module (`home.py`, `page1.py`, `page2.py`) should include both the layout and the callbacks specific to that page.

**`pages/home.py`**:
```python
from dash import html, dcc, Output, Input, State
import dash_mantine_components as dmc

layout = dmc.MantineProvider(
    children=[
        html.H1("Home Page"),
        dcc.Input(id="input-name", type="text", placeholder="Enter your name"),
        html.Button("Submit", id="submit-button"),
        dcc.Link("Go to Page 1", href="/page1"),
        dcc.Link("Go to Page 2", href="/page2")
    ]
)

def register_callbacks(app):
    @app.callback(
        Output("shared-data", "data"),
        Input("submit-button", "n_clicks"),
        State("input-name", "value")
    )
    def update_output(n_clicks, value):
        if n_clicks:
            return {"name": value}
        return {}
```

**`pages/page1.py` and `pages/page2.py`** follow similar structures but display the data:

```python
# For page1.py and page2.py
from dash import html, dcc, Output, Input
import dash_mantine_components as dmc

layout = dmc.MantineProvider(
    children=[
        html.H1("Page 1"),
        html.Div(id="display-name"),
        dcc.Link("Go to Home", href="/")
    ]
)

def register_callbacks(app):
    @app.callback(
        Output("display-name", "children"),
        Input("shared-data", "data")
    )
    def display_name(data):
        name = data.get("name", "No name provided")
        return f"Hello, {name}"
```

#### Step 3: Register the Callbacks

**`pages/__init__.py`**:
This file is used to load all pages and register their callbacks.

```python
def setup_pages(app):
    from . import home, page1, page2
    home.register_callbacks(app)
    page1.register_callbacks(app)
    page2.register_callbacks(app)
```

### Conclusion

By structuring your application in this way, you create a clear separation of concerns, improve the maintainability of your code, and ensure that state is efficiently managed across multiple pages. This approach allows you to scale your application by simply adding new pages and callbacks without disrupting the existing functionality.

### Notes

- `register_callbacks` mechanism.
