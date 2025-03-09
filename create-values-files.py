import argparse
import os
import yaml

def generate_values_yaml(directory: str):
    if not os.path.isdir(directory):
        raise ValueError(f"Provided path is not a directory: {directory}")

    # Ensure the output directories exist
    output_directory = "values-files"
    os.makedirs(output_directory, exist_ok=True)

    # Ensure the channel directory exists
    channel_directory = "channel"
    os.makedirs(channel_directory, exist_ok=True)

    # Create the channel.yaml file
    channel_data = create_channel_yaml(directory)

    # Write channel.yaml to the 'channel' directory
    channel_yaml_path = os.path.join(channel_directory, "channel.yaml")
    with open(channel_yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(channel_data, f, default_flow_style=False, sort_keys=False)

    print(f"Generated {channel_yaml_path}")

    for subdirectory in sorted(os.listdir(directory)):
        subdirectory_path = os.path.join(directory, subdirectory)
        if os.path.isdir(subdirectory_path):
            process_subdirectory(subdirectory_path, output_directory)

def create_channel_yaml(directory: str):
    required_capabilities = []

    # Gather all providedCapabilities from the agent.yaml files
    for subdirectory in sorted(os.listdir(directory)):
        subdirectory_path = os.path.join(directory, subdirectory)
        agent_yaml_path = os.path.join(subdirectory_path, "agent.yaml")

        if os.path.isfile(agent_yaml_path):
            with open(agent_yaml_path, "r", encoding="utf-8") as f:
                agent_info = yaml.safe_load(f)
                provided_capabilities = agent_info.get("providedCapabilities", [])

                for capability in provided_capabilities:
                    # Ensure the capability has a 'name' and 'version' field and only extract those
                    if isinstance(capability, dict) and 'name' in capability and 'version' in capability:
                        required_capabilities.append({
                            "name": capability["name"],  # Use the 'name' field from providedCapabilities
                            "version": capability["version"]  # Use the 'version' field from providedCapabilities
                        })

    # Structure for channel.yaml
    channel_data = {
        "apiVersion": "lmos.eclipse/v1",
        "kind": "Channel",
        "metadata": {
            "name": "acme-web-stable",
            "labels": {
                "tenant": "acme",
                "channel": "web",
                "version": "1.0.0",
                "subset": "stable"
            }
        },
        "spec": {
            "requiredCapabilities": required_capabilities
        }
    }

    return channel_data

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
