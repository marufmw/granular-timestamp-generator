import whisper
import os
import json

# === CONFIG ===
AUDIO_FOLDER = "./audio_files"   # folder containing your 4 audio files
OUTPUT_FOLDER = "./output"       # where TS files will be saved
MODEL_SIZE = "base"              # tiny, base, small, medium, large

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load Whisper model
print("Loading Whisper model...")
model = whisper.load_model(MODEL_SIZE)

def format_word(word):
    return {
        "content": word["word"].strip(),
        "startsAt": round(word["start"], 2),
        "endsAt": round(word["end"], 2),
    }

for file_name in os.listdir(AUDIO_FOLDER):
    if not file_name.endswith((".mp3", ".wav", ".m4a")):
        continue

    file_path = os.path.join(AUDIO_FOLDER, file_name)
    print(f"Processing: {file_name}")

    result = model.transcribe(
        file_path,
        word_timestamps=True
    )

    words = []
    for segment in result["segments"]:
        for word in segment["words"]:
            words.append(format_word(word))

    # Create TypeScript content
    variable_name = os.path.splitext(file_name)[0] + "Words"

    ts_content = "import { Word } from \"@/components/common/audio-text-highlighter\";\n\n"
    ts_content += f"export const {variable_name}: Word[] = [\n"

    for w in words:
        ts_content += f'  {{ content: "{w["content"]}", startsAt: {w["startsAt"]}, endsAt: {w["endsAt"]} }},\n'

    ts_content += "];\n"

    output_file = os.path.join(OUTPUT_FOLDER, variable_name + ".txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ts_content)

    print(f"Saved: {output_file}")

print("Done 🎉")