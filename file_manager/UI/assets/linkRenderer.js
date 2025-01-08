// Make sure we're registering globally
window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

// Debug registration
console.log("START Registering LinkRenderer");

window.dashAgGridComponentFunctions.LinkRenderer = function (props) {
  const { setData, data } = props;
  // Handle case where value is not an object
  if (typeof props.value !== "object" || !props.value) {
    return React.createElement("span", {}, props.value || "");
  }

  // cell value: props.value
  const displayName = props.value.displayName || "";
  const id = props.value.id || {};

  function onClick() {
    // console.log("Link clicked:", id, "data", data, "value", props.value);
    setData(); // Triggers Dash callback
  }

  // If it's a file (has type 'download-link'), render clickable button
  if (id.type === "download-link") {
    return React.createElement(
      "button",
      {
        onClick,
        style: {
          background: "none",
          border: "none",
          color: "blue",
          textDecoration: "underline",
          cursor: "pointer",
          padding: 0,
        },
      },
      displayName
    );
  }

  // If it's a folder or other type
  return React.createElement("span", {}, displayName);
};

console.log(
  "END Registering LinkRenderer:",
  window.dashAgGridComponentFunctions.LinkRenderer
);
