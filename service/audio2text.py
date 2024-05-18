import subprocess
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-small"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)


def convert_video_to_audio(video_path, output_dir='audio_files', output_filename='audio.mp3'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    audio_path = os.path.join(output_dir, output_filename)
    
    command = ['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'libmp3lame', '-b:a', '128k', audio_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return audio_path


def audio2text(sample_path):
    return pipe(sample_path, generate_kwargs={"language": "russian"})['text']