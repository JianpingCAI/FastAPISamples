import jinja2
import json
import sys


def generate_model(model_name, fields, relationships):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("model_template2.j2")

    return template.render(
        model_name=model_name, table_name=model_name.lower(), fields=fields, relationships=relationships
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_models.py <path to model definition JSON>")
        sys.exit(1)

    json_file = sys.argv[1]

    try:
        with open(json_file, "r") as file:
            model_data = json.load(file)

        model_name = model_data["model_name"]
        fields = model_data["fields"]
        relationships = model_data["relationships"]

        output = generate_model(model_name, fields, relationships)

        with open(f"{model_name.lower()}.py", "w") as out_file:
            out_file.write(output)

    except json.JSONDecodeError:
        print("Error: Invalid JSON in the model definition file.")
    except FileNotFoundError:
        print(f"Error: File {json_file} not found.")
    except KeyError as e:
        print(f"Error: Missing key in JSON data - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
