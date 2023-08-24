import PIL
import torch

import hashlib
import os

import numpy as np

from PIL import Image, ImageOps

from .. import path
from ..tree import GIF_BRANCH
import folder_paths


def is_animated(image_path):
    try:
        test_image = Image.open(image_path)
        test_image.seek(1)
    except EOFError:
        return False
    except PIL.UnidentifiedImageError:
        return False
    return True


class TacoImg2ImgAnimatedLoader:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

        return {
            "required": {
                "image": (sorted(files),),
                "frames": ("INT", {"default": 8, "min": 1, "max": 1000})
            },
        }

    CATEGORY = GIF_BRANCH

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"

    def load_image(self, image, frames):
        image_path = folder_paths.get_annotated_filepath(image)
        initial_image = Image.open(image_path)

        images = []
        masks = []

        initial_image = ImageOps.exif_transpose(initial_image)
        image = initial_image.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        if 'A' in initial_image.getbands():
            mask = np.array(initial_image.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        for i in range(frames):
            images.append(image)
            masks.append(mask)

        spread_images = torch.cat(tuple(images), dim=0)
        spread_masks = torch.cat(tuple(masks), dim=1)

        return (spread_images, spread_masks)

    @classmethod
    def IS_CHANGED(s, image, frames):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image, frames):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True


class TacoAnimatedLoader:
    @classmethod
    def INPUT_TYPES(s):
        def animated_filter(image):
            image_path = folder_paths.get_annotated_filepath(image)
            return is_animated(image_path)

        input_dir = folder_paths.get_input_directory()
        files = filter(animated_filter,
                       [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))])

        return {"required":
                    {"image": (sorted(files),)},
                }

    CATEGORY = GIF_BRANCH

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)

        images = []
        # masks = []
        frame_number = 0

        frame = i
        while frame:
            imageI = ImageOps.exif_transpose(frame)
            image = imageI.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            """
            if 'A' in imageI.getbands():
                print("A")
                mask = np.array(imageI.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                print("B")
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            """

            images.append(image)
            # masks.append(mask)

            frame_number += 1
            try:
                frame.seek(frame_number)
            except EOFError:
                break

        spread_images = torch.cat(tuple(images), dim=0)
        # spread_masks = torch.cat(tuple(masks), dim=1)

        return (spread_images,)

    @classmethod
    def IS_CHANGED(s, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        image_path = folder_paths.get_annotated_filepath(image)
        if not is_animated(image_path):
            return "Invalid image type, must be animated"

        return True


class TacoGifMaker:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "frame_rate": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
                "filename_prefix": ("STRING", {"default": "TacoGif"})
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    CATEGORY = GIF_BRANCH
    FUNCTION = "generate_gif"

    def generate_gif(self, images, frame_rate, filename_prefix, prompt=None, extra_pnginfo=None):
        pil_images = []
        for image in images:
            img = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
            pil_images.append(img)

        (
            full_output_folder,
            filename,
            counter,
            subfolder,
            _,
        ) = folder_paths.get_save_image_path(filename_prefix, folder_paths.get_output_directory())

        file = f"{filename}_{counter:05}_.gif"
        file_path = os.path.join(full_output_folder, file)
        pil_images[0].save(
            file_path,
            save_all=True,
            append_images=pil_images[1:],
            duration=round(1000 / frame_rate),
            loop=0,
            compress_level=4
        )

        previews = [
            {
                "filename": file,
                "subfolder": subfolder,
                "type": "output",
            }
        ]
        return {"ui": {"images": previews}}
