from scipy.io.wavfile import write
import io
import ddsp.training
import numpy as np
import pydub
import librosa
import os

SAMPLE_RATE = 16000

def wav_to_np(filepath):
    aseg = pydub.AudioSegment.from_file(filepath, 'wav', start_second=0, duration=5) # 5 sec limit
    aseg = aseg.set_frame_rate(SAMPLE_RATE)
    aseg = aseg.set_channels(1)

    # Convert to numpy array.
    channel_asegs = aseg.split_to_mono()
    #if len(channel_asegs) > 1:
    #    channel_asegs = channel_asegs[0]
    samples = [s.get_array_of_samples() for s in channel_asegs]
    fp_arr = np.array(samples).astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max

    # If only 1 channel, remove extra dim.
    if fp_arr.shape[0] == 1:
        fp_arr = fp_arr[0]

    return fp_arr

def gendrumkit(input_sound, models, savepath):
    print("generating...")

    # Compute audio features
    audio = wav_to_np(input_sound)
    audio_features = ddsp.training.metrics.compute_audio_features(audio)
    audio_features['loudness_db'] = audio_features['loudness_db'].astype(np.float32)

    # hardcoded.. :( 64 for my trained models. TODO: extract from gin file for each model
    hop_size = 64
    time_steps = int(audio.shape[0] / hop_size)
    n_samples = time_steps * hop_size
    for key in ['f0_hz', 'f0_confidence', 'loudness_db']:
        audio_features[key] = audio_features[key][:time_steps]
    audio_features['audio'] = [audio_features['audio'][:n_samples]]

    # go through each trained model and save output to disc
    model_names = list(models.keys())
    for model_name in model_names:
        outputs = models[model_name](audio_features, training=False)
        audio_gen = models[model_name].get_audio_from_outputs(outputs)

        if len(audio_gen.shape) == 2:
            audio_gen = audio_gen[0]

        normalizer = float(np.iinfo(np.int16).max)
        array_of_ints = np.array(np.asarray(audio_gen) * normalizer, dtype=np.int16)
        filepath = os.path.join(savepath, model_name) + '.wav'
        write(filepath, SAMPLE_RATE, array_of_ints)
        
