import time
import os

os.environ["REDIS_URL"] = "redis://localhost:6379"

from dash import Dash, DiskcacheManager, CeleryManager, Input, Output, html, callback

if "REDIS_URL" in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    print(os.environ["REDIS_URL"])
    from celery import Celery

    celery_app = Celery(
        __name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"]
    )
    background_callback_manager = CeleryManager(celery_app)

else:
    # Diskcache for non-production apps when developing locally
    import diskcache

    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, background_callback_manager=background_callback_manager)

app.layout = html.Div(
    [
        html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
        html.Button(id="button_id", children="Run Job!"),
    ]
)


@callback(
    output=Output("paragraph_id", "children"),
    inputs=Input("button_id", "n_clicks"),
    background=True
)
def update_clicks(n_clicks):
    time.sleep(1.0)
    print("debugging...")
    return [f"Clicked {n_clicks} times"]


if __name__ == "__main__":
    app.run(debug=True)
