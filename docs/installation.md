# Installation Guide

This guide provides detailed instructions for installing CommandLAB and its dependencies on different operating systems.

## System Requirements

- **Python**: Python 3.12 or higher
- **Operating System**:
  - Windows 10 or higher
  - macOS 10.14 (Mojave) or higher
  - Ubuntu 18.04 or higher, or other Linux distributions with X11
- **Hardware**:
  - Recommended: 2GB RAM, 1GHz CPU
- **Permissions**:
  - Local control requires permissions to simulate keyboard and mouse input
  - Docker support requires Docker installed and running
  - Cloud deployments require appropriate cloud provider credentials

## Basic Installation

The simplest way to install CommandLAB is using pip:

```bash
pip install commandlab
```

This installs the core framework without specific backends. You'll need to install additional components based on your use case.

## Installation with Backends

### Local Computer Control

To control your local computer, install the local backend:

```bash
pip install "commandlab[local]"
```

This installs dependencies for controlling your local computer:

- `pynput` for keyboard and mouse control
- `pyautogui` for alternative input control
- `mss` for fast screenshots

#### Platform-Specific Notes

**Windows**:

- No additional requirements

**macOS**:

- You may need to grant accessibility permissions to your terminal or Python application
- Go to System Preferences > Security & Privacy > Privacy > Accessibility and add your terminal application

**Linux**:

- X11 is required for input control
- Install X11 dependencies: `sudo apt-get install python3-xlib python3-tk python3-dev`

### Remote Daemon

To use the remote control daemon:

```bash
pip install "commandlab[daemon]"
```

This installs:

- `fastapi` and `uvicorn` for the API server
- `requests` for client communication

### Container Support

For Docker container support:

```bash
pip install "commandlab[docker]"
```

This requires:

- Docker installed and running on your system
- Python Docker SDK

For Kubernetes support:

```bash
pip install "commandlab[kubernetes]"
```

This requires:

- `kubernetes` Python client
- `kubectl` configured with access to a cluster

### Cloud Provider Support

For AWS support:

```bash
pip install "commandlab[aws]"
```

For Azure support:

```bash
pip install "commandlab[azure]"
```

For Google Cloud Platform support:

```bash
pip install "commandlab[gcp]"
```

For all cloud providers:

```bash
pip install "commandlab[cloud]"
```

### Integration Components

For OCR capabilities:

```bash
pip install "commandlab[pytesseract]"
```

This requires:

- Tesseract OCR installed on your system
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

For E2B Desktop integration:

```bash
pip install "commandlab[e2b-desktop]"
```

For LangChain integration:

```bash
pip install "commandlab[langchain]"
```

### All Features

To install all available backends and features:

```bash
pip install "commandlab[all]"
```

Note that this will install all dependencies, which may include conflicting packages. It's generally better to install only the components you need.

## Development Installation

For contributing to CommandLAB:

```bash
# Clone the repository
git clone https://github.com/your-org/commandlab.git
cd commandlab

# Install in development mode with development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Virtual Environment

It's recommended to install CommandLAB in a virtual environment:

```bash
# Create a virtual environment
python -m venv commandlab-env

# Activate the environment
# On Windows:
commandlab-env\Scripts\activate
# On macOS/Linux:
source commandlab-env/bin/activate

# Install CommandLAB
pip install "commandlab[local,daemon]"
```

## Troubleshooting

### Common Issues

#### Permission Errors

**Problem**: `PermissionError` when trying to control mouse or keyboard

**Solution**:

- Run your script with administrator/root privileges
- On macOS, grant accessibility permissions to your terminal
- On Linux, ensure you have the necessary X11 permissions

#### Import Errors

**Problem**: `ImportError: No module named 'pynput'` or similar

**Solution**:

- Ensure you've installed the correct extras: `pip install "commandlab[local]"`
- Check if your virtual environment is activated

#### Docker Issues

**Problem**: `docker.errors.DockerException: Error while fetching server API version`

**Solution**:

- Ensure Docker is installed and running
- Check if your user has permissions to access Docker

#### Cloud Provider Authentication

**Problem**: Authentication errors with cloud providers

**Solution**:

- Ensure you've configured credentials:
  - AWS: Configure AWS CLI or set environment variables
  - Azure: Log in with Azure CLI or set environment variables
  - GCP: Set up application default credentials

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/your-org/commandlab/issues) for similar problems
1. Join our [Discord community](https://discord.gg/your-discord) for support
1. Open a new issue with details about your problem

## Verifying Installation

To verify your installation:

```python
import commandLAB
print(f"CommandLAB version: {commandLAB.__version__}")

# Test local computer if installed
try:
    from commandLAB.computers.local_pynput_computer import LocalPynputComputer
    computer = LocalPynputComputer()
    print("Local computer control is working")
except ImportError:
    print("Local computer control is not installed")
```

## Next Steps

- Follow the [Quick Start Guide](quickstart.md) to begin using CommandLAB
- Explore the [Core Concepts](concepts/index.md) to understand the framework
- Try the [Basic Automation Tutorial](tutorials/basic_automation.md) for a hands-on example
