
# Pattern-Matching Callbac

## Dynamic IDs

## Selectors: ALL, MATCH, ALLSMALLER

Like `ALL`, `MATCH` will fire the callback when any of the component's properties change. However,

- instead of passing all of the values into the callback, `MATCH` will pass just a **single** value into the callback,
- instead of updating a single output, it will update the dynamic output that is "matched" with.
