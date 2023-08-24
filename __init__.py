import filecmp
import os
import shutil

import __main__

from .Nodes.latent_node import TacoLatent
from .Nodes.animated_node import TacoAnimatedLoader, TacoGifMaker, TacoImg2ImgAnimatedLoader

NODE_CLASS_MAPPINGS = {
    "TacoLatent": TacoLatent,
    "TacoAnimatedLoader": TacoAnimatedLoader,
    "TacoImg2ImgAnimatedLoader": TacoImg2ImgAnimatedLoader,
    "TacoGifMaker": TacoGifMaker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TacoLatent": "Taco Latent Image",
    "TacoAnimatedLoader": "Taco Animated Image Loader",
    "TacoImg2ImgAnimatedLoader": "Taco Img2Img Animated Loader",
    "TacoGifMaker": "Taco Gif Maker",
}


def update_javascript():
    extensions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
                                     "web" + os.sep + "extensions" + os.sep + "ComfyUI-TacoNodes")
    javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

    if not os.path.exists(extensions_folder):
        print("Creating frontend extension folder: " + extensions_folder)
        os.mkdir(extensions_folder)

    result = filecmp.dircmp(javascript_folder, extensions_folder)

    if result.left_only or result.diff_files:
        print('Update to javascripts files detected')
        file_list = list(result.left_only)
        file_list.extend(x for x in result.diff_files if x not in file_list)

        for file in file_list:
            print(f'Copying {file} to extensions folder')
            src_file = os.path.join(javascript_folder, file)
            dst_file = os.path.join(extensions_folder, file)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_file)


update_javascript()
