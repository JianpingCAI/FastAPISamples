In Dash applications, callbacks are essential for managing user interactions like handling button clicks, updating data, and controlling component visibility. These callbacks need to be defined **globally** at the application level and registered **before the app starts running**. This means you cannot dynamically register or modify callbacks during runtime; all callbacks must be declared upfront to ensure proper functionality.

Dash expects all components involved in a callback (i.e., `Input`, `Output`, and `State`) to exist in the layout when the app starts. If components are dynamically created as part of a user interaction, their callbacks still need to be predefined. If a callback references components not present at the start, Dash won't automatically register the callback, and it may fail to trigger.

In more complex scenarios, such as dynamic layouts or multi-page apps, you can dynamically change parts of the layout but **not** the callbacks themselves. You need to account for all potential interactions and define corresponding callbacks before launching the app.

For example, you can dynamically update content within the layout (e.g., showing different controls based on user input), but any callback needed to handle that content must already exist. This ensures that Dash handles interactions between components globally and in a predictable manner.

Sources:

- Dash official documentation confirms that all callbacks must be defined before the server starts running and cannot be dynamically registered during runtime.
- The Dash community forum also discusses how dynamic callback registration is not currently supported and callbacks must be declared upfront.
