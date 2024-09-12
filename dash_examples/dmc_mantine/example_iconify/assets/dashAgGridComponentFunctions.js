var dagcomponentfuncs = (window.dashAgGridAPIFunctions =
  window.dashAgGridAPIFunctions || {});

dagcomponentfuncs.DMC_Button = function (props) {
  const { setData, data } = props;

  function onClick() {
    setData();
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
    props.value
  );
};
