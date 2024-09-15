#!/bin/bash

# Function to clean a directory and clone the Git repository, preserving specific subdirectories if needed
clean_and_clone_repo() {
    local dir=$1
    local repo_url=$2
    local preserve_subdir=$3

    # If the directory exists, clean it but preserve the specified subdirectory
    if [ -d "$dir" ]; then
        echo "Cleaning up existing directory $dir, preserving $preserve_subdir..."

        # If the preserve_subdir exists, move it temporarily
        if [ -n "$preserve_subdir" ] && [ -d "$dir/$preserve_subdir" ]; then
            echo "Moving preserved directory $dir/$preserve_subdir to /tmp/$preserve_subdir..."
            mv "$dir/$preserve_subdir" "/tmp/$preserve_subdir" || { echo "Failed to preserve $dir/$preserve_subdir"; exit 1; }
        fi

        # Remove all other contents of the directory
        find "$dir" -mindepth 1 ! -name "$preserve_subdir" -exec rm -rf {} + || { echo "Failed to clean $dir"; exit 1; }
    else
        # Create the directory if it doesn't exist
        mkdir -p "$dir" || { echo "Failed to create directory $dir"; exit 1; }
    fi

    # Clone the repository directly into the target directory
    echo "Cloning $repo_url into $dir..."
    rm -rf "$dir"/*  # Make sure the directory is clean before cloning
    git clone "$repo_url" "$dir" || { echo "Failed to clone $repo_url"; exit 1; }

    # Check if the .git folder exists after cloning
    if [ -d "$dir/.git" ]; then
        echo "Successfully cloned with .git directory present."
    else
        echo "Error: .git directory is missing after clone in $dir."
        exit 1
    fi

    # Move the preserved subdirectory back if it was preserved
    if [ -n "$preserve_subdir" ] && [ -d "/tmp/$preserve_subdir" ]; then
        mv "/tmp/$preserve_subdir" "$dir/$preserve_subdir" || { echo "Failed to restore $dir/$preserve_subdir"; exit 1; }
    fi
}

# Clean and clone the web repository, preserving the users subdirectory
clean_and_clone_repo "./web" "git@github.com:dantweb/loopai-web.git" "users"

# Clean and clone the view repository
clean_and_clone_repo "./view" "git@github.com:dantweb/loopai-view.git"

# Clean and clone the core repository
clean_and_clone_repo "./core" "git@github.com:dantweb/loopai-core.git"

echo "Creating .env files..."
cp .env.dist .env
cp view/vue/admin/.env.dist view/vue/admin/.env

echo "Repositories cleaned, cloned, and ready for development."

# Build and Start Docker services
echo "Building and starting Docker services..."
docker compose up -d --build || { echo "Failed to build and start Docker services"; exit 1; }

echo "Installation and startup complete."

cd ..
