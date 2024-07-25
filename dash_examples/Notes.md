# Notes

```bash

export REACT_VERSION=18.2.0


```

## Layout

- html: HTML components
- dcc: Dash core components
- dbc: Dash bootstrap components
- dmc: Dash Mantine components

## Callbacks

- Input
- Output
- State

### with State

### Auto Component IDs

- not work with dynamic callback content unless the component variables are defined out of the callback scope.
- not compatible with Pattern-Matching Callbacks

### Rules

- Dash Callbacks must never modify variables outside of their scope.
- Dash is stateless. With a stateless framework, user sessions are not mapped 1-1 with server processes. Each `callback request` can be executed on any of the available server processes.
- When Dash apps run across multiple workers, their memory is not shared. This means that if you modify a global variable in one callback, that modification will not be applied to the other workers/processes.

### Share Variable / State Between Callbacks

- multiple outputs

#### Storing Shared Data

To share data safely across multiple processes/servers,

- In the user's browser session, using `dcc.Store`
- - `example2_dcc.Store`
- On the disk (e.g., file or database)
- In server-side memory (RAM) shared across processes and servers such as Redis database
- Flask cache

### Pattern-Matching Callbacks
