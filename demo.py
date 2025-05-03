from PIL import Image
from transformers import CLIPTokenizer
import torch
import model_loader
import pipeline

# Global progress tracking
progress_percent = 0

def generate_from_prompt(prompt, progress_callback=None):
    global progress_percent
    progress_percent = 0

    DEVICE = "cpu"
    ALLOW_CUDA = False
    ALLOW_MPS = False

    if ALLOW_CUDA and torch.cuda.is_available():
        DEVICE = "cuda"
    elif ALLOW_MPS and torch.backends.mps.is_built() and torch.backends.mps.is_available():
        DEVICE = "mps"

    tokenizer = CLIPTokenizer("vocab.json", merges_file="merges.txt")
    model_file = "v1-5-pruned-emaonly.ckpt"
    models = model_loader.preload_models_from_standard_weights(model_file, DEVICE)

    # Generation settings
    uncond_prompt = ""
    do_cfg = True
    cfg_scale = 8
    input_image = None
    strength = 0.9
    sampler = "ddpm"
    num_inference_steps = 50
    seed = 42

    # Call the pipeline with progress callback
    output_image = pipeline.generate(
        prompt=prompt,
        uncond_prompt=uncond_prompt,
        input_image=input_image,
        strength=strength,
        do_cfg=do_cfg,
        cfg_scale=cfg_scale,
        sampler_name=sampler,
        n_inference_steps=num_inference_steps,
        seed=seed,
        models=models,
        device=DEVICE,
        idle_device="cpu",
        tokenizer=tokenizer,
        progress_updater=progress_callback
    )

    return Image.fromarray(output_image)
