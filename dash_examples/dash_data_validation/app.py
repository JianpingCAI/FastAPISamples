from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
from validators import (
    validate_name,
    validate_age,
    validate_email,
    validate_date_of_birth,
    validate_postal_code,
)
import base64
from typing import Tuple, Optional, List

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Input(
            id="input-name",
            type="text",
            placeholder="Enter your name",
            className="input-field",
        ),
        dcc.Input(
            id="input-age",
            type="number",
            placeholder="Enter your age",
            className="input-field",
        ),
        dcc.Input(
            id="input-email",
            type="email",
            placeholder="Enter your email",
            className="input-field",
        ),
        dcc.Input(
            id="input-dob",
            type="text",
            placeholder="Enter your birth date (YYYY-MM-DD)",
            className="input-field",
        ),
        dcc.Checklist(
            id="has-postal-code",
            options=[{"label": "I have a postal code", "value": "yes"}],
            value=[],
        ),
        dcc.Input(
            id="input-postal-code",
            type="text",
            placeholder="Enter your postal code",
            disabled=True,
            className="input-field",
        ),
        dcc.Upload(
            id="upload-file",
            children=html.Button("Upload File"),
            className="input-field",
        ),
        html.Button(id="submit-button", children="Submit"),
        html.Div(id="output-div", className="output-message"),
    ]
)


@app.callback(
    Output("input-postal-code", "disabled"), Input("has-postal-code", "value")
)
def toggle_postal_code_input(has_postal_code: List[str]) -> bool:
    """Enables or disables postal code input based on checkbox selection."""
    return "yes" not in has_postal_code


def validate_file(contents: Optional[str], filename: Optional[str]) -> Tuple[bool, str]:
    """Validates the uploaded file based on extension and size."""
    if contents is None or filename is None:
        return True, "No file uploaded."  # No file is a valid case

    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return False, "Only .png, .jpg, and .jpeg files are allowed."

    content_string = contents.split(",")[1]  # Ignore content_type as it’s unused
    decoded = base64.b64decode(content_string)

    if len(decoded) > 1e6:  # 1 MB limit
        return False, "File is too large. Maximum size is 1MB."

    return True, filename


@app.callback(
    Output("output-div", "children"),
    Output("output-div", "className"),
    Input("submit-button", "n_clicks"),
    State("input-name", "value"),
    State("input-age", "value"),
    State("input-email", "value"),
    State("input-dob", "value"),
    State("has-postal-code", "value"),
    State("input-postal-code", "value"),
    State("upload-file", "contents"),
    State("upload-file", "filename"),
)
def validate_and_submit(
    n_clicks: Optional[int],
    name: Optional[str],
    age: Optional[str],
    email: Optional[str],
    dob: Optional[str],
    has_postal_code: List[str],
    postal_code: Optional[str],
    file_contents: Optional[str],
    filename: Optional[str],
) -> Tuple[str, str]:
    if n_clicks is None:
        return "", ""

    errors = []

    # Name validation
    is_valid_name, name_msg = validate_name(name)
    if not is_valid_name:
        errors.append(name_msg)

    # Age validation
    is_valid_age, age_msg = validate_age(age)
    if not is_valid_age:
        errors.append(age_msg)

    # Email validation
    is_valid_email, email_msg = validate_email(email)
    if not is_valid_email:
        errors.append(email_msg)

    # Date of Birth validation
    is_valid_dob, dob_msg = validate_date_of_birth(dob)
    if not is_valid_dob:
        errors.append(dob_msg)

    # Postal code validation (if required)
    if "yes" in has_postal_code:
        is_valid_postal, postal_msg = validate_postal_code(postal_code)
        if not is_valid_postal:
            errors.append(postal_msg)

    # File validation
    is_valid_file, file_msg = validate_file(file_contents, filename)
    if not is_valid_file:
        errors.append(file_msg)

    # Return errors if any, otherwise success
    if errors:
        return "\n".join(errors), "error-message"

    return "All inputs are valid! Form submitted successfully.", "success-message"


if __name__ == "__main__":
    app.run_server(debug=True)
