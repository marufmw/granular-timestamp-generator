# Granular Timestamp Generator

A utility project that uses OpenAI's Whisper model to transcribe audio files and generate granular word-level timestamps. The output can be used for audio-text synchronization features like word highlighting during playback.

## Overview

This project takes audio files (MP3, WAV, or M4A) and generates timestamped word data using Whisper's word-level timestamps. The output includes:
- **content**: The word/phrase spoken
- **startsAt**: Start timestamp in seconds
- **endsAt**: End timestamp in seconds

## Prerequisites

1. **Python 3.8+** installed
2. **FFmpeg** installed (required for audio processing)
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from https://ffmpeg.org/download.html

## Installation

1. **Clone or navigate to the project directory**

2. **Install required Python packages**

```bash
pip install openai-whisper ffmpeg-python
```

Or with uv:

```bash
uv pip install openai-whisper ffmpeg-python
```

## Project Structure

```
granular-timestamp-generator/
├── generate.py           # Main script for transcription
├── audio_files/         # Place your audio files here
│   ├── AuditorySense.mp3
│   ├── Proprioception.mp3
│   ├── VisualSense.mp3
│   └── WrapUp.mp3
├── output/              # Generated timestamp files
│   ├── AuditorySenseWords.txt
│   └── ...
└── README.md
```

## Usage

### Step 1: Add Your Audio Files

Place your audio files in the [`audio_files/`](audio_files) directory. Supported formats:
- `.mp3`
- `.wav`
- `.m4a`

### Step 2: Configure the Script

Edit [`generate.py`](generate.py) to customize settings:

| Variable | Description | Options |
|----------|-------------|---------|
| `AUDIO_FOLDER` | Path to audio files | Default: `./audio_files` |
| `OUTPUT_FOLDER` | Path for output files | Default: `./output` |
| `MODEL_SIZE` | Whisper model size | `tiny`, `base`, `small`, `medium`, `large` |

For faster processing, use `tiny` or `base`. For better accuracy, use `small` or `medium`.

### Step 3: Run the Script

```bash
python generate.py
```

The script will:
1. Load the Whisper model
2. Process each audio file in the `audio_files` folder
3. Generate timestamped word data
4. Save the output to the `output` folder

### Step 4: Use the Output

The generated files contain TypeScript arrays that can be imported into your project:

```typescript
import { AuditorySenseWords } from "./output/AuditorySenseWords";
```

## Output Format

Each generated file contains an array of word objects:

```typescript
import { Word } from "@/components/common/audio-text-highlighter";

export const AuditorySenseWords: Word[] = [
  { content: "Hello", startsAt: 0.0, endsAt: 0.5 },
  { content: "world", startsAt: 0.6, endsAt: 1.0 },
  // ...
];
```

## Model Size Comparison

| Model | Parameters | English-only | Multilingual | Required VRAM | Relative Speed |
|-------|------------|--------------|--------------|---------------|----------------|
| tiny  | 39M        | ✅           | ✅           | ~1 GB         | ~32x           |
| base  | 74M        | ✅           | ✅           | ~1 GB         | ~16x           |
| small | 244M       | ✅           | ✅           | ~2 GB         | ~6x            |
| medium| 769M       | ✅           | ✅           | ~5 GB         | ~2x            |
| large | 1550M      | ✅           | ✅           | ~10 GB        | 1x             |

**Recommendation**: Start with `base` for a good balance of speed and accuracy.

## Troubleshooting

### FFmpeg not found
If you get an error about FFmpeg, make sure it's installed and available in your PATH:
```bash
ffmpeg -version
```

### CUDA/GPU Support
For GPU acceleration, install PyTorch with CUDA support first:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
Then run the script - Whisper will automatically use GPU if available.

### Memory Issues
If you run into memory problems, switch to a smaller model:
```python
MODEL_SIZE = "tiny"  # or "base"
```

## License

MIT License
