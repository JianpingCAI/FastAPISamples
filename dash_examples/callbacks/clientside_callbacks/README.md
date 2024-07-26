# Client-Side Callbacks

<https://dash.plotly.com/clientside-callbacks>

## Introduction

Sometimes callbacks can incur a significant overhead, especially when they:

- receive and/or return very large quantities of data (transfer time)
- are called very often (network latency, queuing, handshake)
- are part of a callback chain that requires multiple roundtrips between the browser and Dash

When the overhead cost of a callback becomes too great and no other optimization is possible, the callback can be modified to be run directly in the browser instead of a making a request to Dash.

The syntax for the callback is almost exactly the same; you use Input and Output as you normally would when declaring a callback, but you also define a **JavaScript function** as the first argument to the @callback decorator.

## Limitations

There are a few limitations to keep in mind:

- Clientside callbacks execute on the browser's main thread and will block rendering and events processing while being executed.

- Clientside callbacks are not possible if you need to refer to global variables on the server or a DB call is required.

- Dash versions prior to 2.4.0 do not support asynchronous clientside callbacks and will fail if a Promise is returned.
