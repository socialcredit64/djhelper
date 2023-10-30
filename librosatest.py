import librosa


filename = "song.wav"

f2 = "whmd.mp3"
f3 = r"C:\Users\S2184895\Downloads\Leon's mission\Eva Shaw - Space Jungle (Showtek Intro Edit).mp3"

y, sr = librosa.load(f3)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print("Tempo: {:.2f}".format(tempo)) 
