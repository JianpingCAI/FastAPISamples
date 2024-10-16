from dash import Dash, html


import os
from dash_iconify import DashIconify
import dash_mantine_components as dmc


class FileTree:
    def __init__(self, filepath: os.PathLike, id: str):
        """
        Usage: component = FileTree('Path/to/my/File').render()
        """
        self.id = id
        self.filepath = filepath

    def render(self) -> dmc.Accordion:
        return dmc.Accordion(
            FileTree.build_tree(self.filepath, isRoot=True), id=self.id, multiple=True
        )

    @staticmethod
    def flatten(l):
        return [item for sublist in l for item in sublist]

    @staticmethod
    def make_file(file_name):
        return dmc.Text(
            [DashIconify(icon="akar-icons:file"), " ", file_name],
            style={"paddingTop": "5px"},
        )

    @staticmethod
    def make_folder(folder_name):
        return [DashIconify(icon="akar-icons:folder"), " ", folder_name]

    @staticmethod
    def build_tree(path, isRoot=False):
        d = []
        if os.path.isdir(path):  # if it is a folder
            children = [
                FileTree.build_tree(os.path.join(path, x)) for x in os.listdir(path)
            ]
            print(children)
            if isRoot:
                return FileTree.flatten(children)
            item = dmc.AccordionItem(
                [
                    dmc.AccordionControl(FileTree.make_folder(os.path.basename(path))),
                    dmc.AccordionPanel(children=FileTree.flatten(children)),
                ],
                value=path,
            )
            d.append(item)

        else:
            d.append(FileTree.make_file(os.path.basename(path)))
        return d


app = Dash(__name__)

import dash_bootstrap_components as dbc

tree = FileTree(".", "file_tree").render()


app.layout = html.Div(
    [
        html.H1("Hello Dash"),
        dbc.Button("Select folder", id="select_folder", className="mr-1"),
        tree,
    ]
)
from dash.dependencies import Input, Output

import subprocess


@app.callback(
    Output("file_tree", "children"),
    [Input("select_folder", "n_clicks")],
)
def add(n_clicks):
    if n_clicks > 0:
        command = ["python", "./local.py"]
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        out, err = p.communicate()
        print(out, err)
        path = out.decode("utf-8").strip()
        children = FileTree.build_tree(path, isRoot=True)
        print(children)
        return children


if __name__ == "__main__":
    app.run_server(debug=True)
