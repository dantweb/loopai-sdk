#!/bin/bash

# Function to clean a directory and clone the Git repository, preserving specific subdirectories
clean_and_clone_repo() {
    local dir=$1
    local repo_url=$2
    local preserve_subdir=$3
    local temp_dir="/tmp/$(basename $dir)"  # Define a temporary directory for cloning

    # If the directory exists, clean it but preserve the specified subdirectory
    if [ -d "$dir" ]; then
        echo "Cleaning up existing directory $dir, preserving $preserve_subdir..."

        # If the preserve_subdir exists, move it temporarily
        if [ -n "$preserve_subdir" ] && [ -d "$dir/$preserve_subdir" ]; then
            echo "Copying preserved directory $dir/$preserve_subdir to /tmp/$preserve_subdir..."
            mv "$dir/$preserve_subdir" "/tmp/$preserve_subdir" || { echo "Failed to preserve $dir/$preserve_subdir"; exit 1; }
        fi

        echo "Remove all contents of the directory $dir..."
        # Remove all contents of the directory
        rm -rf "$dir"/* "$dir"/.[!.]* "$dir"/..?* || { echo "Failed to clean $dir"; exit 1; }
    fi

    # Clone the repository into the temporary directory
    echo "Cloning $repo_url into $temp_dir..."
    rm -rf "$temp_dir"  # Ensure the temp directory is clean
    git clone "$repo_url" "$temp_dir" || { echo "Failed to clone $repo_url"; exit 1; }

    # Copy the cloned contents into the target directory
    cp -r "$temp_dir"/* "$dir/" || { echo "Failed to copy cloned contents to $dir"; exit 1; }

    # Clean up the temporary directory
    rm -rf "$temp_dir"

    # Move the preserved subdirectory back if it was preserved
    if [ -n "$preserve_subdir" ] && [ -d "/tmp/$preserve_subdir" ]; then
        mv "/tmp/$preserve_subdir" "$dir/$preserve_subdir" || { echo "Failed to restore $dir/$preserve_subdir"; exit 1; }
    fi
}

cd ..
# Clean and clone the web repository, preserving the users subdirectory
clean_and_clone_repo "./web" "git@github.com:dantweb/loopai-web.git" "users"

# Clean and clone the view repository
clean_and_clone_repo "./view" "git@github.com:dantweb/loopai-view.git"

# Clean and clone the core repository
clean_and_clone_repo "./core" "git@github.com:dantweb/loopai-core.git"

echo "Repositories cleaned and updated successfully."

# Build and Start Docker services
echo "Building and starting Docker services..."
docker compose up -d --build || { echo "Failed to build and start Docker services"; exit 1; }

# Run the Flask application inside the web container
echo "Starting Flask application..."
docker compose exec web flask --app web/web_interface run || { echo "Failed to start Flask application"; exit 1; }

echo "Installation and startup complete."
