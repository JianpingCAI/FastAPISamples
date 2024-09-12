var dagcomponentfuncs = (window.dashAgGridAPIFunctions =
  window.dashAgGridAPIFunctions || {});

console.log("dashAgGridAPIFunctions loaded");

dagcomponentfuncs.SomeLink = function (props) {
  return React.createElement(
    "a",
    { href: "https://finance.yahoo.com/quote/" + props.value },
    props.value
  );
};

dagcomponentfuncs.MyButton = function (props) {
  const { setData, data } = props;

  function onClick() {
    setData();
  }
  return React.createElement(
    "button",
    {
      onClick: onClick,
      className: props.className,
    },
    props.value
  );
};

dagcomponentfuncs.DMC_Action_Button = function (props) {
  const { setData, data } = props;
  // console.log(props);

  function onClick() {
    setData({
      action: props.action,
      data: data,
    });
  }

  let leftSection, rightSection;
  if (props.leftIcon) {
    leftSection = React.createElement(window.dash_iconify.DashIconify, {
      icon: props.leftIcon,
    });
  }
  if (props.rightIcon) {
    rightSection = React.createElement(window.dash_iconify.DashIconify, {
      icon: props.rightIcon,
    });
  }
  return React.createElement(
    window.dash_mantine_components.Button,
    {
      onClick,
      variant: props.variant,
      color: props.color,
      leftSection: leftSection,
      rightSection: rightSection,
      radius: props.radius,
      style: {
        margin: props.margin,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      },
    },
    props.action
  );
};

dagcomponentfuncs.DMC_EditSave_Button = function (props) {
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
      data: props.data,
      // edit_mode: new_edit_mode,
      action: props.action
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
