# 🐭 Shy Cursor

A cursor that runs away from your hand like a scared animal.

## What it does

- Wanders your screen when left alone
- Flees when your index finger approaches
- Panics when cornered against an edge
- Freezes for 2 seconds if you "catch" it
- Then teleports somewhere else, startled
- Calms down after 8 seconds without threats

## Requirements

- Python 3.9+
- A webcam
- Windows, macOS, or Linux

## Installation

pip install -r requirements.txt

On macOS, grant Accessibility permission:
System Settings → Privacy & Security → Accessibility → enable your terminal.

## Run

python main.py

## Controls

- Q (in the debug window) — quit
- Move your index finger toward the cursor to chase it

## How It Works

- MediaPipe Hands tracks your fingertip at 30 FPS.
- A tiny state machine gives the cursor moods:
  calm → wary → panicked → frozen → calm.
- PyAutoGUI moves the actual OS cursor each frame.

## Notes

- PyAutoGUI's failsafe is disabled — press Q in the debug window to stop.
- Only the primary monitor is used.

## License

MIT