<<<<<<< HEAD
# Gesture OS

A gesture-based operating system interface that allows you to control your computer using hand gestures.

## Features

- **Real-time Gesture Recognition**: Uses MediaPipe to detect hand gestures from your webcam
- **System Control**: Map gestures to system actions like clicking, scrolling, volume control, and app switching
- **Modern UI**: Clean, dark-themed interface built with PyQt5
- **Cross-platform**: Supports macOS, Linux, and Windows

## Gesture Mappings

- **Fist**: No action
- **Point (Index finger)**: Mouse click
- **Peace (Two fingers)**: Scroll
- **Three fingers**: Switch applications
- **Four fingers**: Volume up
- **Open hand**: Volume down

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

1. The intro screen will appear first
2. Click "Start Gesture OS" to begin
3. Position your hand in front of the camera
4. Perform gestures to control your system

## Requirements

- Python 3.7 or higher
- Webcam/camera access
- Required Python packages (see `requirements.txt`)

## System Dependencies

### macOS
- No additional system dependencies required

### Linux
- `xdotool` for mouse/keyboard simulation: `sudo apt-get install xdotool`
- `amixer` (usually pre-installed) for volume control

### Windows
- PowerShell (pre-installed)

## Project Structure

```
gesture_os/
├── main.py                 # Application entry point
├── ui/                     # User interface components
│   ├── intro_screen.py    # Welcome screen
│   ├── main_window.py     # Main application window
│   └── styles.py          # UI styling
├── core/                   # Core gesture recognition
│   ├── gesture_thread.py  # Background gesture detection thread
│   └── gesture_classifier.py  # Gesture classification logic
├── services/               # System integration
│   └── action_mapper.py   # Maps gestures to system actions
└── assets/                # Future assets (icons, etc.)
```

## Development

This project uses:
- **PyQt5**: For the graphical user interface
- **OpenCV**: For camera access and image processing
- **MediaPipe**: For hand landmark detection and gesture recognition

## License

This project is open source and available for modification and distribution.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

=======
# GestureOS
AI-powered gesture-based OS controller using computer vision and machine learning for real-time, hands-free system interaction.
>>>>>>> 93b136271d4826ed9ad692dfa5073107d531e26b
