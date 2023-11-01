import librosa



f3 = r"C:\Users\X571LH\Downloads\Leon's mission\Usher - Scream (Luke Alexander _ Angelo The Kid Remix).wav"

y, sr = librosa.load(f3)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print("Tempo: {:.2f}".format(tempo)+"\n") 
print(tempo)
