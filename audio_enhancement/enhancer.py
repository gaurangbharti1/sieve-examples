import sieve

valid_tasks = ["upsample", "noise", "all"]

metadata = sieve.Metadata(
    title="Audio Enhancer",
    description="Remove background noise from audio and upsample to 48kHz.",
    code_url="https://github.com/sieve-community/examples/tree/main/audio_enhancement",
    image=sieve.Image(
        url="https://storage.googleapis.com/sieve-public-data/audio_noise_reduction/cover.png"
    ),
    tags=["Audio", "Speech", "Enhancement", "Featured"],
    readme=open("README.md", "r").read(),
)


@sieve.function(name="audio_enhancement", metadata=metadata)
def enhance_audio(audio: sieve.Audio, filter_type: str = "all"):
    '''
    :param audio: An audio input (mp3 and wav supported)
    :param filter_type: Task to perform, one of ["upsample", "noise", "all"]
    :return: Enhanced audio
    '''
    audio_format = audio.path.split('.')[-1]
    if audio_format not in ['mp3', 'wav']:
        raise ValueError("Audio format must be mp3 or wav")

    task = filter_type.strip().lower()
    if task not in valid_tasks:
        raise ValueError(f"Task must be one of {valid_tasks}")

    enhance_func = sieve.function.get("sieve/audiosr")
    denoise_func = sieve.function.get("sieve/deepfilternet_v2")

    if task == "upsample":
        return enhance_func.run(audio)
    elif task == "noise":
        return denoise_func.run(audio)
    return denoise_func.run(enhance_func.run(audio))
