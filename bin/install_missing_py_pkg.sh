#!/bin/bash

# Define a list of Python's standard library modules
standard_libs=$(python -c "import sys; import pkgutil; print('\n'.join([mod.name for mod in pkgutil.iter_modules()]))")

# List all installed packages
installed_packages=$(pip freeze | cut -d '=' -f 1)

# Extract all imported packages from .py files
imported_packages=$(grep -hrE "^(import|from) " /app/*.py | \
    sed -E 's/from ([^ ]+) .*/\1/; s/import ([^,]+).*/\1/; s/, /\n/g' | \
    awk '{print $1}' | sort -u)

# Find packages that are not installed and are not standard libraries
missing_packages=()
for package in $imported_packages; do
    # Skip standard library modules and any known Python reserved words or modules that don't need installation
    if echo "$standard_libs" | grep -qw "$package" || python -c "import $package" &> /dev/null; then
        continue
    fi

    # Check if the package is installed
    if ! echo "$installed_packages" | grep -q "^$package$"; then
        # Adjust package names if needed (e.g., dotenv should be python-dotenv)
        if [ "$package" == "dotenv" ]; then
            package="python-dotenv"
        fi
        missing_packages+=($package)
    fi
done

# Install missing packages
if [ ${#missing_packages[@]} -ne 0 ]; then
    echo "Installing missing packages: ${missing_packages[@]}"
    pip install --no-cache-dir "${missing_packages[@]}"
else
    echo "All required packages are already installed."
fi
