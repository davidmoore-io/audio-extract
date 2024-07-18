#!/bin/bash

# Define variables
INSTALL_DIR="$HOME/.audio-extract"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_NAME="audio_extract.py"
WRAPPER_NAME="audio-extract"
GITHUB_RAW_URL="https://raw.githubusercontent.com/davidmoore-io/audio-extract/master"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Download the main script
curl -o "$INSTALL_DIR/$SCRIPT_NAME" "$GITHUB_RAW_URL/audio_extract.py"

# Create virtual environment
python3 -m venv "$VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install required packages
pip install yt-dlp

# Create wrapper script
cat > "$INSTALL_DIR/$WRAPPER_NAME" << EOL
#!/bin/bash
source "$VENV_DIR/bin/activate"
python "$INSTALL_DIR/$SCRIPT_NAME" "\$@"
EOL

# Make wrapper script executable
chmod +x "$INSTALL_DIR/$WRAPPER_NAME"

# Add to PATH
echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$HOME/.zshrc"
echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$HOME/.bash_profile"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install ffmpeg using Homebrew
brew install ffmpeg

echo "Installation complete. Please restart your terminal or run 'source ~/.zshrc' (or 'source ~/.bash_profile' for bash) to use audio-extract."