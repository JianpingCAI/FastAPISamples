# Callbacks

## When Are Callbacks Executed?

This section describes the circumstances under which the **dash-renderer** front-end client can make a request to the Dash **back-end server** (or the **clientside callback code**) to execute a callback function.

### When a Dash App First Loads

All of the callbacks in a Dash app are executed with the initial value of their inputs when the app is first loaded. This is known as the "initial call" of the callback. To learn how to suppress this behavior, see the documentation for the prevent_initial_call attribute of Dash callbacks.

It is important to note that when a Dash app is initially loaded in a web browser by the dash-renderer front-end client, its entire callback chain is introspected recursively.

This allows the dash-renderer to predict the order in which callbacks will need to be executed, as callbacks are blocked when their inputs are outputs of other callbacks which have not yet fired. In order to unblock the execution of these callbacks, first callbacks whose inputs are immediately available must be executed. This process helps the dash-renderer to minimize the time and effort it uses, and avoid unnecessarily redrawing the page, by making sure it only requests that a callback is executed when all of the callback's inputs have reached their final values.

### As a Direct Result of User Interaction

### As an Indirect Result of User Interaction

### When Dash Components Are Added to the Layout

It is possible for a callback to insert new Dash components into a Dash app's layout. If these new components are themselves the inputs to other callback functions, then their appearance in the Dash app's layout will trigger those callback functions to be executed.

## Circular Callbacks

As of dash v1.19.0, you can create circular updates **within the same callback**.

Circular callback chains that involve *multiple* callbacks are **not** supported.

Circular callbacks can be used to keep multiple inputs synchronized to each other.

