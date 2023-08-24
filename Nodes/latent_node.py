import torch

from ..tree import TRUNK

ratio_map = {
    "1:1": [512, 512],
    "3:4": [416, 576],
    "4:3": [576, 416],
    "9:16": [384, 672],
    "16:9": [672, 384]
}
resolution_map = {
    "small (512)": 1,
    "medium (1024)": 2,
    "large (2048)": 4
}


class TacoLatent:
    aspect_ratios = ["1:1", "3:4", "4:3", "9:16", "16:9"]
    resolution_ratios = ["small (512)", "medium (1024)", "large (2048)"]

    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (cls.aspect_ratios,),
                "resolution_ratio": (cls.resolution_ratios,),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"

    CATEGORY = TRUNK

    def generate(self, aspect_ratio, resolution_ratio, batch_size=1):
        ratio = ratio_map[aspect_ratio]
        resolution_multiplier = resolution_map[resolution_ratio]
        latent = torch.zeros(
            [batch_size, 4, (ratio[1] * resolution_multiplier) // 8, (ratio[0] * resolution_multiplier) // 8]
        )
        return ({"samples": latent},)
