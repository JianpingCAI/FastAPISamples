from dataclasses import dataclass, asdict
import dash
from dash import Dash, dcc, Input, Output, State, html, MATCH, ALL
from dash_ag_grid import AgGrid
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from dash import ctx
from UI.api_client import fetch_root_nodes, fetch_child_nodes, create_node, upload_file, fetch_child_file_nodes, fetch_child_folder_nodes, download_file, delete_node
import base64
import json
from dash_iconify import DashIconify
from backend.schemas import NodeDataORM, NodeDataCreate, FileMetadata
from typing import List, Dict, Any, Optional, Union

# Initialize app
app: Dash = Dash(__name__, suppress_callback_exceptions=True)


@dataclass
class FileSystemOperation:
    operation: str
    id: str
    parent_node_id: str
    name: str
    description: str

    def to_json(self):
        return json.dumps(asdict(self))

    def from_json(json_str: str):
        data = json.loads(json_str)
        return FileSystemOperation(**data)


def create_modal_for_new_folder(accord_id: str, node_id: str) -> dmc.Modal:
    return dmc.Modal(
        id={"type": "modal", "node_id": node_id, "node_type": "folder"},
        children=[
            dmc.Title("Add Folder", order=3),
            dmc.Stack(
                [
                    dmc.TextInput(
                        id={"type": "modal-input", "node_id": node_id, "node_type": "folder", "field": "name"},
                        label="Name",
                        required=True,
                    ),
                    dmc.Textarea(
                        id={"type": "modal-input", "node_id": node_id, "node_type": "folder", "field": "description"},
                        label="Description",
                    ),
                    dmc.Group(
                        [
                            dmc.Button(
                                "Close",
                                id={"type": "modal-close", "node_id": node_id, "node_type": "folder"},
                                variant="outline",
                            ),
                            dmc.Button(
                                "Save",
                                id={"type": "modal-save", "node_id": node_id, "node_type": "folder"},
                                variant="filled",
                            ),
                        ]
                    ),
                ]
            ),
        ],
        opened=False,
    )


def create_modal_for_new_file(node_id: str, parent_node_id) -> dmc.Modal:
    return dmc.Modal(
        id={"type": "modal", "node_id": node_id, "node_type": "file"},
        children=[
            dcc.Store(id={"type": "dccstore-file-node-operation", "node_id": node_id}, data=None),
            dmc.Title("Add File", order=3),
            dmc.Stack(
                [
                    # upload file control
                    dcc.Upload(
                        id={"type": "modal-upload", "node_id": node_id},
                        children=html.Div(["Drag and Drop or", html.A("Select a file")]),
                        multiple=False,
                        style={
                            "width": "80%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px",
                        },
                    ),
                    # show uploaded file name
                    dmc.TextInput(
                        id={"type": "modal-input", "node_id": node_id, "node_type": "file", "field": "name"},
                        label="Name",
                        required=True,
                        readOnly=True,
                    ),
                    dmc.Textarea(
                        id={"type": "modal-input", "node_id": node_id, "node_type": "file", "field": "description"},
                        label="Description",
                    ),
                    # dmc.Text(
                    #     id={"type": "modal-status", "node_id": modal_id}, size="sm"
                    # ),
                    dmc.Group(
                        [
                            dmc.Button(
                                "Close",
                                id={"type": "modal-close", "node_id": node_id, "node_type": "file"},
                                variant="outline",
                            ),
                            dmc.Button(
                                "Save",
                                id={"type": "modal-save", "node_id": node_id, "node_type": "file"},
                                variant="filled",
                            ),
                        ]
                    ),
                ]
            ),
        ],
        opened=False,
    )


def create_delete_folder_confirmation_modal(parent_accord_id: str, node_id: str) -> dmc.Modal:
    return dmc.Modal(
        id={"type": "modal-delete-confirm", "accord_id": parent_accord_id, "node_id": node_id},
        title="Confirm Deletion",
        children=[
            dmc.Text("Are you sure you want to delete this folder? This action cannot be undone."),
            dmc.Space(h=20),
            dmc.Group(
                [
                    dmc.Button(
                        "Cancel",
                        variant="outline",
                        id={"type": "button-delete-cancel", "accord_id": parent_accord_id, "node_id": node_id},
                    ),
                    dmc.Button(
                        "Delete",
                        color="red",
                        variant="filled",
                        id={"type": "button-delete-confirm", "accord_id": parent_accord_id, "node_id": node_id},
                    ),
                ],
            ),
        ],
        opened=False,
    )


# Update columnDefs with proper HTML rendering configuration
columnDefs = [
    {"field": "id", "hide": True},
    {
        "field": "name",
        "headerName": "Name",
        "filter": True,
        # Make sure name matches exactly with JS registration
        "cellRenderer": "LinkRenderer",
        "autoHeight": True,
    },
    {"field": "description", "headerName": "Description", "filter": True},
]


def convert_node_to_dict(node: NodeDataORM) -> Dict[str, Any]:
    node_dict = {}
    node_dict["id"] = node.id
    if node.is_folder:
        node_dict["name"] = node.name  # Simple string for folders
    else:
        # Special link format for files
        node_dict["name"] = {"displayName": node.name, "id": {"type": "download-link", "node_id": node.id}}
    node_dict["description"] = node.description
    return node_dict


def convert_nodes(nodes: List[NodeDataORM]) -> List[Dict[str, Any]]:
    converted_nodes = []
    for node in nodes:
        node_dict = convert_node_to_dict(node)
        converted_nodes.append(node_dict)
    return converted_nodes


def create_aggrid_files(node_id: str, nodes: List[NodeDataORM]) -> AgGrid:
    converted_nodes = convert_nodes(nodes) if nodes else []

    # Create hidden download links for each file
    hidden_links = []
    for node in nodes:
        if not node.is_folder:
            hidden_links.append(
                html.A(
                    id={"type": "download-link", "node_id": node.id},
                    style={"display": "none"},
                )
            )

    return html.Div(
        [
            *hidden_links,
            AgGrid(
                id={"type": "aggrid", "node_id": node_id},
                columnDefs=columnDefs,
                rowData=converted_nodes,
                dashGridOptions={
                    "pagination": False,
                    "suppressCellSelection": True,
                    "domLayout": "autoHeight",
                },
                getRowId="params.data.id",
                columnSize="sizeToFit",
                defaultColDef={"resizable": True},
                dangerously_allow_code=True,
            ),
        ]
    )


# Create accordion item, dmc.AccordionItem --> dmc.AccordionControl & dmc.AccordionPanel
def create_accordion_item(parent_accord_id: str, node: NodeDataORM) -> dmc.AccordionItem:
    if not node.is_folder:
        return dmc.AccordionItem()  ## TODO

    """Create an accordion item for a given node."""
    # Only show add buttons for folders
    action_controls = [
        dmc.Group(
            [
                dcc.Store(id={"type": "dccstore-folder-node-operation", "node_id": node.id}, data=None),
                create_modal_for_new_folder(accord_id=node.id, node_id=node.id),
                create_modal_for_new_file(
                    node_id=node.id,
                    parent_node_id=node.parent_id if node.parent_id else "root",
                ),
                create_delete_folder_confirmation_modal(parent_accord_id=parent_accord_id, node_id=node.id),
                # Add file
                dmc.Tooltip(
                    label="Add file",
                    children=dmc.ActionIcon(
                        children=DashIconify(icon="mdi:file-plus"),
                        id={"type": "button-add-file", "node_id": node.id},
                        size="lg",
                        variant="light",
                    ),
                ),
                # Add folder
                dmc.Tooltip(
                    label="Add subfolder",
                    children=dmc.ActionIcon(
                        children=DashIconify(icon="mdi:folder-plus"),
                        id={"type": "button-add-folder", "node_id": node.id},
                        size="lg",
                        variant="light",
                    ),
                ),
                # Delete a folder
                dmc.Tooltip(
                    label="Delete folder",
                    children=dmc.ActionIcon(
                        children=DashIconify(icon="mdi:folder-remove"),
                        id={"type": "button-delete-folder", "accord_id": parent_accord_id, "node_id": node.id},
                        size="lg",
                        variant="light",
                        color="red",
                    ),
                ),
            ],
            gap="xs",
            justify="right",
        )
    ]

    sub_file_nodes = fetch_child_file_nodes(parent_id=node.id)
    files_grid = create_aggrid_files(node_id=node.id, nodes=sub_file_nodes)

    return dmc.AccordionItem(
        # id={"type": "accordion-item", "node_id": node.id, "accord_id": accord_id},
        value=node.id,
        children=[
            dmc.AccordionControl(
                id={"type": "accordion-control", "node_id": node.id, "node_name": node.name},
                children=dmc.Group(
                    [
                        dmc.Text(f"{node.name}"),
                        dmc.Text(f"{node.description}") if node.description else None,
                        *action_controls,
                    ],
                    justify="apart",
                    gap="xs",
                    grow=True,
                ),
            ),
            dmc.AccordionPanel(
                id={"type": "accordion-panel", "node_id": node.id, "accord_id": parent_accord_id},
                children=html.Div(
                    id={"node_id": node.id},
                    children=[
                        files_grid,
                        create_accordion(accord_id=node.id, node_id=node.id, nodes=[]),
                    ],
                ),
            ),
        ],
        loading_state={
            "type": "dot",
            "is_loading": False,
            "component_name": f"accordion-{node.id}",
        },
    )


# dmc.Accordion -->[dmc.AccordionItem] --> dmc.AccordionControl & dmc.AccordionPanel
def create_accordion(accord_id: str, node_id: str, nodes: List[NodeDataORM]) -> dmc.Accordion:
    """Create an accordion from a list of nodes."""

    accordion_items = []
    if len(nodes) > 0:
        accordion_items = [create_accordion_item(parent_accord_id=accord_id, node=node) for node in nodes if node.is_folder]

    accordion = dmc.Accordion(
        id={"type": "accordion", "accord_id": accord_id, "node_id": node_id},
        children=[
            dcc.Store(id={"type": "dccstore-accordion-loaded_node_ids", "accord_id": accord_id}, data=[]),
            dcc.Store(id={"type": "dccstore-accordion-load_node_id", "accord_id": accord_id}, data=None),
            *accordion_items,
        ],
        multiple=False,
        chevronPosition="left",
        value=[],  # Track expanded items
    )

    return accordion


# Fetch root nodes for the initial view
root_nodes: List[NodeDataORM] = fetch_root_nodes()

# Fix LoadingOverlay usage in layout
app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "light",
        "primaryColor": "blue",
        "components": {"Modal": {"styles": {"modal": {"minWidth": 500}}}},
    },
    children=[
        dmc.Container(
            [
                # dcc.Store(id={"type": "dccstore-node_to_load"}, data=None),
                dmc.Title("Reference Data Management", order=1),
                dmc.Group(
                    [
                        dmc.Button(
                            "Add Folder",
                            id={"type": "button-add-folder", "node_id": "root"},
                            variant="filled",
                        ),
                    ],
                    mt="md",
                    mb="md",
                ),
                dmc.Box(
                    # create an accordion
                    children=[create_accordion(accord_id="root", node_id="root", nodes=root_nodes)],
                    pos="relative",
                ),
                # modal for creating a new folder
                dcc.Store(id={"type": "dccstore-folder-node-operation", "node_id": "root"}, data=None),
                create_modal_for_new_folder(accord_id="root", node_id="root"),
                dmc.Notification(
                    id="notification-root",  # Changed from pattern to string ID
                    autoClose=5000,
                    title="",
                    message="",
                    style={"display": "none"},
                    action="show",
                ),
                dcc.Download(id="download"),
            ]
        )
    ],
)


##################################################################################
# Callbacks
##################################################################################


# Save folder
@app.callback(
    [
        Output({"type": "modal", "node_id": MATCH, "node_type": "folder"}, "opened", allow_duplicate=True),
        Output({"type": "dccstore-folder-node-operation", "node_id": MATCH}, "data"),
    ],
    Input({"type": "modal-save", "node_id": MATCH, "node_type": "folder"}, "n_clicks"),
    State({"type": "modal-input", "node_id": MATCH, "field": "name", "node_type": "folder"}, "value"),
    State({"type": "modal-input", "node_id": MATCH, "field": "description", "node_type": "folder"}, "value"),
    prevent_initial_call=True,
)
def handle_modal_save_folder(n_save, name, description):
    if not ctx.triggered_id:
        raise PreventUpdate

    parent_node_id = ctx.triggered_id.get("node_id", "")
    if not parent_node_id:
        raise PreventUpdate

    if not name:
        raise PreventUpdate

    try:
        new_data = NodeDataCreate(name=name, is_folder=True, description=description, parent_id=None if parent_node_id == "root" else parent_node_id)
        created_node: NodeDataORM = create_node(new_data)
        operation = FileSystemOperation(operation="add_folder", id=created_node.id, parent_node_id=parent_node_id, name=name, description=description).to_json()

        print(f"handle_modal_save_folder: {operation}")
        return False, operation

    except Exception as e:
        raise PreventUpdate


@app.callback(
    Output({"type": "accordion", "accord_id": ALL, "node_id": MATCH}, "children", allow_duplicate=True),
    Input({"type": "dccstore-folder-node-operation", "node_id": MATCH}, "data"),  # id of the new node
    State({"type": "accordion", "accord_id": ALL, "node_id": MATCH}, "children"),
    prevent_initial_call=True,
)
def handle_add_new_folder(_, list_old_children):
    # if not data:
    #     raise PreventUpdate

    if len(ctx.triggered) != 1:
        raise PreventUpdate

    data = ctx.triggered[0].get("value", None)
    if not data:
        raise PreventUpdate

    accord_id = ctx.triggered_id["node_id"]

    print(f"handle_add_new_folder: {ctx.triggered_id}")
    operation: FileSystemOperation = FileSystemOperation.from_json(data)

    new_data = NodeDataORM(
        id=operation.id,
        name=operation.name,
        is_folder=True,
        description=operation.description,
        parent_node_id=(None if operation.parent_node_id == "root" else operation.parent_node_id),
    )
    accordion_old_children: List[dmc.AccordionItem] = list_old_children[0]
    new_item: dmc.AccordionItem = create_accordion_item(parent_accord_id=accord_id, node=new_data)
    accordion_new_children = [new_item] + accordion_old_children
    return [accordion_new_children]


@app.callback(
    Output({"type": "dccstore-accordion-loaded_node_ids", "accord_id": MATCH}, "data"),
    Output({"type": "accordion-panel", "node_id": ALL, "accord_id": MATCH}, "children"),  # Note: it is the parent accordion ID
    Input({"type": "accordion", "accord_id": MATCH, "node_id": ALL}, "value"),
    State({"type": "dccstore-accordion-loaded_node_ids", "accord_id": MATCH}, "data"),
    State({"type": "accordion-panel", "node_id": ALL, "accord_id": MATCH}, "id"),  # Note: it is the parent accordion ID
    State({"type": "accordion-panel", "node_id": ALL, "accord_id": MATCH}, "children"),  # Note: it is the parent accordion ID
    prevent_initial_call=True,
)
def handle_load_subitems_of_folder(_, loaded_node_ids, list_panel_ids, list_panel_children):
    """Fetch children when accordion item is expanded"""
    if not ctx.triggered_id or len(ctx.triggered) != 1:
        raise PreventUpdate

    expanded_node_ids = ctx.triggered[0].get("value", [])
    if len(expanded_node_ids) == 0:
        raise PreventUpdate

    loaded_node_ids = [] if not loaded_node_ids else loaded_node_ids

    for node_id in expanded_node_ids:
        if node_id not in loaded_node_ids:

            # find the index of the panel to update
            panel_index = -1
            for index, item in enumerate(list_panel_ids):
                if item["node_id"] == node_id:
                    panel_index = index
                    break

            if panel_index == -1:
                raise PreventUpdate

            loaded_nodes: List[NodeDataORM] = fetch_child_folder_nodes(parent_id=node_id)
            if len(loaded_nodes) == 0:
                raise PreventUpdate

            new_accordion = create_accordion(accord_id=node_id, node_id=node_id, nodes=loaded_nodes)

            list_new_panel_children = [dash.no_update] * len(list_panel_children)
            list_new_panel_children[panel_index] = list_panel_children[panel_index]
            list_new_panel_children[panel_index]["props"]["children"][1] = new_accordion

            loaded_node_ids.append(node_id)
            print(f"handle_load_subitems_of_folder: {ctx.triggered_id}, {node_id}")

            return loaded_node_ids, list_panel_children

    raise PreventUpdate


# show uploaded file name
@app.callback(
    Output({"type": "modal-input", "node_id": MATCH, "node_type": "file", "field": "name"}, "value"),
    Input({"type": "modal-upload", "node_id": MATCH}, "filename"),
    prevent_initial_call=True,
)
def show_uploaded_file_name(filename):
    if not filename:
        raise PreventUpdate

    return filename


# upload a file, and add it to a folder
@app.callback(
    Output({"type": "modal", "node_id": MATCH, "node_type": "file"}, "opened", allow_duplicate=True),
    Output({"type": "aggrid", "node_id": MATCH}, "rowTransaction"),
    Input({"type": "modal-save", "node_id": MATCH, "node_type": "file"}, "n_clicks"),
    [
        State({"type": "modal-input", "node_id": MATCH, "field": "name", "node_type": "file"}, "value"),
        State({"type": "modal-input", "node_id": MATCH, "field": "description", "node_type": "file"}, "value"),
        State({"type": "modal-upload", "node_id": MATCH}, "contents"),
    ],
    prevent_initial_call=True,
)
def handle_modal_save_file(_, name, description, file_contents):
    if not ctx.triggered_id:
        raise PreventUpdate

    parent_node_id = ctx.triggered_id.get("node_id", None)
    if not parent_node_id:
        raise PreventUpdate

    if not name:
        raise PreventUpdate

    try:
        # upload file
        file_metadata = FileMetadata(name=name, description=description, parent_id=parent_node_id)
        created_file_node: NodeDataORM = upload_file(file_contents, file_metadata)
        aggrid_row = created_file_node.model_dump()
        aggrid_row = convert_node_to_dict(created_file_node)
        return False, {"add": [aggrid_row]}

    except Exception as e:
        print(f"ERROR - handle_modal_save_file: {e}")
        raise PreventUpdate


# Show modal: add a new folder
@app.callback(
    Output(
        {"type": "modal", "node_id": MATCH, "node_type": "folder"},
        "opened",
        allow_duplicate=True,
    ),
    Input({"type": "button-add-folder", "node_id": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_popup_modal_create_subfolder(n_clicks):
    # print(f"handle_popup_modal_create_subfolder: {ctx.triggered_id}")

    if n_clicks:
        return True
    raise PreventUpdate


# Show modal: add a new file
@app.callback(
    Output(
        {"type": "modal", "node_id": MATCH, "node_type": "file"},
        "opened",
        allow_duplicate=True,
    ),
    Input({"type": "button-add-file", "node_id": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def show_modal_subfile(n_clicks):
    print(f"show_modal_subfile: {ctx.triggered_id}")

    if n_clicks:
        return True
    raise PreventUpdate


@app.callback(
    Output({"type": "modal-delete-confirm", "accord_id": MATCH, "node_id": MATCH}, "opened", allow_duplicate=True),
    Input({"type": "button-delete-folder", "accord_id": MATCH, "node_id": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_show_delete_confirmation(n_clicks):
    if n_clicks:
        return True
    raise PreventUpdate


@app.callback(
    [
        Output({"type": "modal-delete-confirm", "accord_id": MATCH, "node_id": ALL}, "opened", allow_duplicate=True),
        Output({"type": "accordion", "accord_id": MATCH, "node_id": ALL}, "children", allow_duplicate=True),
    ],
    [
        Input({"type": "button-delete-confirm", "accord_id": MATCH, "node_id": ALL}, "n_clicks"),  # parent id, current node id
        Input({"type": "button-delete-cancel", "accord_id": MATCH, "node_id": ALL}, "n_clicks"),
    ],
    [
        State({"type": "accordion", "accord_id": MATCH, "node_id": ALL}, "children"),
        State({"type": "modal-delete-confirm", "accord_id": MATCH, "node_id": ALL}, "id"),  # Add state to get number of modals
    ],
    prevent_initial_call=True,
)
def handle_delete_folder(confirm_clicks, cancel_clicks, parent_children, modal_ids):
    """Handle the confirmation of folder deletion."""
    triggered_id = ctx.triggered_id
    if not triggered_id:
        raise PreventUpdate

    # Get number of modals to close (needed for correct length of return list)
    num_modals = len(modal_ids)

    # Handle cancel button
    if triggered_id.get("type") == "button-delete-cancel":
        return [False] * num_modals, [dash.no_update]

    # Handle confirm button
    if triggered_id.get("type") == "button-delete-confirm":
        delete_folder_id = triggered_id.get("node_id", None)

        if not delete_folder_id:
            print("ERROR - handle_delete_folder: Could not find folder ID")
            return [False] * num_modals, [dash.no_update]

        try:
            # Delete the folder through API
            is_success = delete_node(delete_folder_id)
            if not is_success:
                print(f"ERROR - handle_delete_folder: Failed to delete folder {delete_folder_id}")
                return [False] * num_modals, [dash.no_update]

            # Remove the folder from UI
            accordion_children = parent_children[0]
            updated_children = [child for child in accordion_children if not (isinstance(child, dict) and child.get("props", {}).get("value") == delete_folder_id)]

            return [False] * num_modals, [updated_children]

        except Exception as e:
            print(f"ERROR - handle_delete_folder: {str(e)}")
            return [False] * num_modals, [dash.no_update]

    raise PreventUpdate


# Close modal for folders
@app.callback(
    Output({"type": "modal", "node_id": MATCH, "node_type": "folder"}, "opened"),
    Input({"type": "modal-close", "node_id": MATCH, "node_type": "folder"}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_modal_close_folder(n_close):
    """Handle all modal-related operations for folders"""

    print(f"handle_modal_close_folder: {ctx.triggered_id}")
    if not ctx.triggered_id:
        raise PreventUpdate

    # Handle modal close
    return False


# Handle file downloads
@app.callback(
    Output("download", "data"),
    Input({"type": "aggrid", "node_id": ALL}, "cellRendererData"),
    prevent_initial_call=True,
)
def handle_download_file(cellRendererData):
    if not ctx.triggered_id or len(ctx.triggered) != 1:
        raise PreventUpdate

    row_data = ctx.triggered[0].get("value", None)
    if not row_data:
        raise PreventUpdate

    file_id = row_data["rowId"]
    file_name = row_data.get("displayName", f"download_{file_id}")  # Use actual filename from grid
    file_content = download_file(file_id)

    if isinstance(file_content, str):
        file_content = file_content.encode("utf-8")

    return dcc.send_bytes(file_content, filename=file_name)


# Close modal for files
@app.callback(
    Output({"type": "modal", "node_id": MATCH, "node_type": "file"}, "opened"),
    Input({"type": "modal-close", "node_id": MATCH, "node_type": "file"}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_modal_close_file(n_close):
    """Handle all modal-related operations for files"""
    print(f"handle_modal_close_file: {ctx.triggered_id}")
    if not ctx.triggered_id:
        raise PreventUpdate

    return False
    # Handle modal close


if __name__ == "__main__":
    app.run_server(debug=True)
