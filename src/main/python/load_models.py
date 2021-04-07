import gin
import ddsp
import ddsp.training
import tensorflow.compat.v2 as tf
import os

model_dirs = {
    'kick': './models/kick/',
    'clap': './models/clap/',
    'snare': './models/snare/',
    'openhat': './models/openhat/',
    'closedhat': './models/closedhat/',
    'tom': './models/tom/',
    'rimshot': './models/rimshot/',
    'cymbal': './models/cymbal/',
}

def load():
    ddsp.spectral_ops.reset_crepe()
    model_names = list(model_dirs.keys())
    models = {}
    for model in model_names:
        gin_file = os.path.join(model_dirs[model], 'operative_config-0.gin')
        with gin.unlock_config():
            gin.parse_config_file(gin_file, skip_unknown=True)
        ckpt_files = [f for f in tf.io.gfile.listdir(model_dirs[model]) if 'ckpt' in f]
        ckpt_name = ckpt_files[0].split('.')[0]
        ckpt = os.path.join(model_dirs[model], ckpt_name)
        models[model] = ddsp.training.models.Autoencoder()
        models[model].restore(ckpt)
        print(model + " loaded")

    return models
