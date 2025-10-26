# Mpv Title

Write the title and artist of a playlist's current song to `~/.mpv-title.txt`.

## Setup

Run the following commands in the top level of the project.

```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Run the following commands in the top level of the project.

```
source venv/bin/activate
python main.py
```

## Dev Help

### Resources

[python-mpv docs](https://github.com/jaseg/python-mpv)
[mpv properties](https://mpv.io/manual/master/#properties)

### Environment Variables

Print debug information (might be buggy).

```
DEBUG_MODE=. python main.py
```

Write output to a different file.

```
OUTPUT_FILE="[path to your file]" python main.py
```
