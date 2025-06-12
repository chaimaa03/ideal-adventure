import numpy as np
import mne
from scipy import stats

def extract_features_from_edf(file_path):
    # Load and preprocess EEG
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    raw.set_eeg_reference()
    raw.filter(l_freq=1, h_freq=45)

    # Get first epoch (or average over epochs if you prefer)
    epochs = mne.make_fixed_length_epochs(raw, duration=25, overlap=0).get_data()

    if epochs.shape[0] == 0:
        raise ValueError("No epochs found in EEG file")

    epoch = epochs[0]  # Shape: (19, 6250)

    # --- Feature extraction ---
    def mean(data): return np.mean(data, axis=-1)
    def std(data): return np.std(data, axis=-1)
    def ptp(data): return np.ptp(data, axis=-1)
    def var(data): return np.var(data, axis=-1)
    def minim(data): return np.min(data, axis=-1)
    def maxim(data): return np.max(data, axis=-1)
    def argminim(data): return np.argmin(data, axis=-1)
    def argmaxim(data): return np.argmax(data, axis=-1)
    def mean_square(data): return np.mean(data**2, axis=-1)
    def rms(data): return np.sqrt(np.mean(data**2, axis=-1))
    def abs_diffs_signal(data): return np.sum(np.abs(np.diff(data, axis=-1)), axis=-1)
    def skewness(data): return stats.skew(data, axis=-1)
    def kurtosis(data): return stats.kurtosis(data, axis=-1)

    # Concatenate features
    features = np.concatenate([
        mean(epoch), std(epoch), ptp(epoch), var(epoch),
        minim(epoch), maxim(epoch), argminim(epoch), argmaxim(epoch),
        mean_square(epoch), rms(epoch), abs_diffs_signal(epoch),
        skewness(epoch), kurtosis(epoch)
    ])

    return features.reshape(1, -1)  # Shape (1, 247)
