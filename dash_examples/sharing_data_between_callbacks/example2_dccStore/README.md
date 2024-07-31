
```bash

export REACT_VERSION=18.2.0

python app.py

```

or,

```bash

export REACT_VERSION=18.2.0

gunicorn example2_dccStore.app:server --reload --log-level debug

```

## dcc.Location component for URL routing

dcc.Location Component: Used to track the URL and trigger page navigation.

Callbacks for Navigation: The callback in app.py updates the content of the page-content div based on the URL.

## dcc.Store for storing data

dcc.Store Component: Stores data in the browser's local storage or session storage.
This data is accessible across different callbacks.

### Note

The data needs to be serialized into a JSON string before being stored in the browser's local storage or session storage.
