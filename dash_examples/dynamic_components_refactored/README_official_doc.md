<https://dash.plotly.com/callback-gotchas#all-callbacks-must-be-defined-before-the-server-starts>

## All callbacks must be defined before the server starts

**All your callbacks** must be defined before your Dash app's server starts running, which is to say, before you call `app.run(debug=True)`.

This means that while you can assemble changed layout fragments dynamically during the handling of a callback, you **can't define dynamic callbacks** in response to user input during the handling of a callback. If you have a dynamic interface, where a callback changes the layout to include a different set of input controls, then you must have already defined the callbacks required to service these new controls in advance.

For example, a common scenario is a Dropdown component that updates the current layout to replace a dashboard with another logically distinct dashboard that has a different set of controls (the number and type of which might which might depend on other user input) and different logic for generating the underlying data. A sensible organization would be for each of these dashboards to have separate callbacks. In this scenario, each of these callbacks much then be defined before the app starts running.

Generally speaking, if a feature of your Dash app is that the number of Inputs or States is determined by a user's input, then you must predefine every permutation of callback that a user can potentially trigger. For an example of how this can be done programmatically using the callback decorator, see this Dash Community forum post.
