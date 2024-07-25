
# Example 3 - Caching and Signaling

[Doc](https://dash.plotly.com/sharing-data-between-callbacks)

This example:

- Uses Redis via Flask-Cache for storing “global variables” on the server-side in a database. This data is accessed through a function (global_store()), the output of which is cached and keyed by its input arguments.

- Uses the dcc.Store solution to send a signal to the other callbacks when the expensive computation is complete.

- Note that instead of Redis, you could also save this to the file system. See <https://flask-caching.readthedocs.io/en/latest/> for more details.

- This **“signaling”** is performant because it allows the expensive computation to only take up one process and be performed once. Without this type of signaling, each callback could end up computing the expensive computation in parallel, locking four processes instead of one.

Another benefit of this approach is that future sessions can use the pre-computed value. This will work well for apps that have a small number of inputs.

## Notes

- This example cached computations in a way that was **accessible for all users**.

- We've simulated an expensive process by using a system sleep of 3 seconds. When the app loads, it takes three seconds to render all four graphs. The initial computation only blocks one process.

- Once the computation is complete, the signal is sent and four callbacks are executed **in parallel** to render the graphs. Each of these callbacks retrieves the data from the "global server-side store": the Redis or filesystem cache.

- We've set processes=6 in app.run so that multiple callbacks can be executed in parallel. In production, this is done with something like `$ gunicorn --workers 6 app:server`. If you don't run with multiple processes, then you won't see the graphs update in parallel as callbacks will be updated serially.

- As we are running the server with multiple processes, we set threaded to False. A Flask server can't be both multi-process and multi-threaded.

- Selecting a value in the dropdown will take less than three seconds if it has already been selected in the past. This is because the value is being pulled from the cache.

- Similarly, reloading the page or opening the app in a new window is also fast because the initial state and the initial expensive computation has already been computed.
