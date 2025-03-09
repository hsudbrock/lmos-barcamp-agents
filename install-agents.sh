#!/bin/bash

# Directory containing the YAML files
VALUES_DIR="values-files"

# Ensure the values directory exists
if [ ! -d "$VALUES_DIR" ]; then
  echo "Directory $VALUES_DIR does not exist!"
  exit 1
fi

# Iterate over all YAML files in the values directory
for values_file in "$VALUES_DIR"/*.yaml; do
  # Extract the base name of the values file (without extension)
  release_name=$(basename "$values_file" .yaml)

  # Remove the "values-" prefix from the release name
  release_name="${release_name#values-}"

  # Check if the values file exists
  if [ -f "$values_file" ]; then
    # Create the Helm release using the values file
    echo "Creating Helm release for $release_name using $values_file"

    # Replace the 'my-helm-chart' with the actual chart you want to deploy
    helm upgrade --install "$release_name" oci://ghcr.io/hsudbrock/arc-base-chart --version 0.1.0-SNAPSHOT -f "$values_file" --set image.pullPolicy=Always

    # Check if the helm command was successful
    if [ $? -eq 0 ]; then
      echo "Helm release $release_name created successfully."
    else
      echo "Error creating Helm release $release_name."
    fi
  else
    echo "No YAML file found at $values_file"
  fi
done
