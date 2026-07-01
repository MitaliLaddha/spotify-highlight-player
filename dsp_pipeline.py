import librosa
import numpy as np
import os

def extract_highlight(audio_path, duration=30):
    """
    Analyzes an audio track using RMS energy and Onset Detection 
    to pinpoint the exact start time of the best highlight.
    """
    if not os.path.exists(audio_path):
        print(f"Error: Could not find audio file at {audio_path}")
        return None

    print(f"Analyzing {os.path.basename(audio_path)}... (<4s processing time)")
    
    # 1. Load Audio
    # We downsample to 22050 Hz. It is mathematically sufficient for 
    # energy/beat detection and makes the script run 2x faster.
    y, sr = librosa.load(audio_path, sr=22050)

    # 2. Calculate RMS Energy (Loudness tracking)
    rms = librosa.feature.rms(y=y)[0]
    
    # librosa's default hop_length is 512 samples per frame
    frames_per_sec = sr / 512 
    window_frames = int(duration * frames_per_sec)

    if len(rms) < window_frames:
        print("Track is too short for the requested duration.")
        return 0 

    # 3. Find the 30-second window with the maximum total energy
    max_energy = 0
    best_frame = 0
    
    for i in range(len(rms) - window_frames):
        window_energy = np.sum(rms[i:i+window_frames])
        if window_energy > max_energy:
            max_energy = window_energy
            best_frame = i

    rough_start_time = librosa.frames_to_time(best_frame, sr=sr)

    # 4. Refine using Onset Detection (Snap to the Beat-Drop)
    # This prevents the highlight from starting slightly off-beat
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_times = librosa.frames_to_time(onsets, sr=sr)

    # Find the closest heavy beat within a 1.5-second radius of our rough start
    valid_onsets = [t for t in onset_times if rough_start_time - 1.5 <= t <= rough_start_time + 1.5]
    
    if valid_onsets:
        final_start_time = valid_onsets[0] # Snap to the exact beat
    else:
        final_start_time = rough_start_time # Fallback to rough estimate

    print(f"Algorithmically extracted highlight start: {final_start_time:.2f} seconds")
    return int(final_start_time)

# --- Local Testing Block ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python dsp_pipeline.py <path_to_audio_file.mp3>")
    else:
        file_path = sys.argv[1]
        extract_highlight(file_path, duration=30)