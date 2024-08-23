// assets/home.js
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside = {
  home_function: function (n_clicks) {
    if (n_clicks) {
      return "Home button clicked " + n_clicks + " times";
    }
    return "";
  },
};
