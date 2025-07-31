from flask import Flask, request, jsonify
import tempfile
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("tiny")  # Gunakan "tiny.en" jika hanya bahasa Inggris

# Daftar target jawaban
SOAL_TARGETS = [
    ["안녕하세요", "안녕하세요!", "안녕하세요."],
    ["안녕히 계세요", "안녕히 계세요!", "안녕히 계세요."],
    ["안녕히 가세요", "안녕히 가세요!", "안녕히 가세요."],
    ["감사합니다", "감사합니다!", "감사합니다."],
    ["죄송합니다", "죄송합니다!", "죄송합니다."],
    ["사랑해요", "사랑해요!", "사랑해요."],
    ["주세요", "주세요!", "주세요."],
    ["알겠어요", "알겠어요!", "알겠어요."],
    ["모르겠어요", "모르겠어요!", "모르겠어요."],
    ["고맙습니다", "고맙습니다!", "고맙습니다."],
]

# Variabel global soal
current_soal_index = 0  

@app.route('/recognize', methods=['POST'])
def recognize():
    global current_soal_index

    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"status": "error", "message": "Missing audio"}), 400

    if current_soal_index >= len(SOAL_TARGETS):
        return jsonify({"status": "finished", "message": "Semua soal telah selesai"}), 200

    target_texts = SOAL_TARGETS[current_soal_index]

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_file.save(temp_audio.name)
            audio_path = temp_audio.name

        result = model.transcribe(audio_path, language="ko")
        recognized_text = result.get("text", "").strip()
        os.remove(audio_path)

        print(f"Recognized Speech: {recognized_text}")
        print(f"Target Variations for Soal {current_soal_index + 1}: {target_texts}")

        is_correct = any(t in recognized_text for t in target_texts)

        if is_correct:
            current_soal_index += 1
            print(f"Jawaban benar! Pindah ke soal {current_soal_index + 1}")

        return jsonify({
            "status": "success",
            "recognized": recognized_text,
            "match": is_correct,
            "next_soal": current_soal_index + 1 if current_soal_index < len(SOAL_TARGETS) else "selesai"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/reset', methods=['POST'])
def reset():
    global current_soal_index
    current_soal_index = 0
    print("Soal direset ke 1.")
    return jsonify({"status": "reset", "current_soal": current_soal_index + 1})
