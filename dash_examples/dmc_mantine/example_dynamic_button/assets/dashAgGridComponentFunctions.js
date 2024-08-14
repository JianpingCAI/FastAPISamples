var dagcomponentfuncs = (window.dashAgGridComponentFunctions =
  window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.DMC_Action_Button = function (props) {
  console.log("props.data = " + JSON.stringify(props.data, null, 2));
  console.log("props.data.edit_mode = " + props.data.edit_mode);

  const [buttonText, setButtonText] = React.useState(
    props.data.edit_mode === true ? "Save" : "Edit" // previous edit_mode value
  );

  function onClick() {
    console.log("buttonText1 = " + buttonText);
    const new_buttonText = buttonText === "Edit" ? "Save" : "Edit";

    const new_edit_mode = buttonText === "Edit" ? true : false;
    console.log("new_edit_mode = " + new_edit_mode);

    setButtonText(new_buttonText);
    console.log("new_buttonText = " + new_buttonText);

    props.setData({
      ...props.data,
      // edit_mode: new_edit_mode,
    });

    // console.log("pros.setData: " + JSON.stringify(props.data, null, 2));
  }

  return React.createElement(
    window.dash_mantine_components.Button,
    {
      onClick,
      style: {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      },
    },
    buttonText
  );
};
