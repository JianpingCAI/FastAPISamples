import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from presentation.ui.pages import home, blog, post, user, login

# Add the root directory to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up the layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Blogs", href="/blogs")),
                dbc.NavItem(dbc.NavLink("Login", href="/login")),
            ],
            brand="Blog Platform",
            color="primary",
            dark=True,
        ),
        html.Div(id="page-content"),
    ]
)


# Define the callback to control page navigation
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/blogs":
        return blog.layout
    elif pathname.startswith("/post/"):
        return post.layout
    elif pathname.startswith("/user/"):
        return user.layout
    elif pathname == "/login":
        return login.layout
    else:
        return home.layout


# Expose the Flask server instance
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
