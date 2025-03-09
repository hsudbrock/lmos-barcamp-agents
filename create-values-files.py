import argparse
import os
import yaml

def generate_values_yaml(directory: str):
    if not os.path.isdir(directory):
        raise ValueError(f"Provided path is not a directory: {directory}")

    # Ensure the output directory exists
    output_directory = "values-files"
    os.makedirs(output_directory, exist_ok=True)

    for subdirectory in sorted(os.listdir(directory)):
        subdirectory_path = os.path.join(directory, subdirectory)
        if os.path.isdir(subdirectory_path):
            process_subdirectory(subdirectory_path, output_directory)

def process_subdirectory(subdirectory: str, output_directory: str):
    agents = {}
    agent_info = {}
    agent_yaml_path = os.path.join(subdirectory, "agent.yaml")

    if os.path.isfile(agent_yaml_path):
        with open(agent_yaml_path, "r", encoding="utf-8") as f:
            agent_info = yaml.safe_load(f)

    for filename in sorted(os.listdir(subdirectory)):
        if filename.endswith(".kts"):  # Only process .kts files
            file_path = os.path.join(subdirectory, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    agents[filename] = f.read()

    values = {
        "lmos": {
            "enabled": True,
            "description": agent_info.get("description", ""),
            "supportedChannels": agent_info.get("supportedChannels", []),
            "providedCapabilities": agent_info.get("providedCapabilities", [])
        },
        "arc": {
            "agents": agents
        }
    }

    output_file = os.path.join(output_directory, f"values-{os.path.basename(os.path.abspath(subdirectory))}.yaml")

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(values, f, default_flow_style=False, sort_keys=False)

    print(f"Generated {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate values.yaml for each subdirectory containing agent script files.")
    parser.add_argument("directory", type=str, help="Parent directory containing subdirectories with agent scripts.")
    args = parser.parse_args()

    generate_values_yaml(args.directory)
