import librosa


def extract_audio(audio, sr=8000):
    wav, sample_rate = librosa.load(audio, sr=sr)
    dur = float(len(wav) / sample_rate)
    channel = len(wav.shape)
    print(f"Audio has {channel} channels")
    wav_return = wav
    return wav_return
