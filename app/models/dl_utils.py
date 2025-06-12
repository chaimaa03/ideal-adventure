import mne
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained DL model once
dl_model = load_model('app/models/schizo_model.keras')  # adjust path if needed

def preprocess_edf_for_dl(file_path):
    raw = mne.io.read_raw_edf(file_path, preload=True)
    raw.set_eeg_reference()
    raw.filter(l_freq=1., h_freq=45.)

    # Take one epoch for now (adjust duration as used in training)
    epochs = mne.make_fixed_length_epochs(raw, duration=25, overlap=0)
    data = epochs.get_data()  # shape = (n_epochs, 19, 6250)

    if data.shape[0] == 0:
        raise ValueError("No EEG data found in the file.")

    # Reshape first epoch for prediction: (1, 6250, 19)
    first_epoch = data[0].transpose()  # shape = (6250, 19)
    return first_epoch[np.newaxis, :, :]  # shape = (1, 6250, 19)
