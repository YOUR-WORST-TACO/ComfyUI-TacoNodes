# ComfyUI-TacoNodes

A handful of nodes I created for my own purposes, they do the following:

- [Taco Latent Image]()
  - A replacement for the standard **Empty Latent Image** intended for faster latent image creation.
- [Taco Animated Image Loader]()
  - Loads an animated image and batches each frame for processing.
- [Taco Img2Img Animated Loader]()
  - Loads a standard image and creates a batch for processing.
- [Taco Gif Maker]()
  - Takes a collection of images and combines them into a gif.

## Taco Latent Image

I made this to simplify my tweaking of workflows in ComfyUI as I found having to remember exact pixel measurements 
frustrating and inconvenient

To use this you first select an aspect ratio, then select a scale for that ratio which will multiply the aspect ratio

### Aspect Ratios
This is a list of the following Aspect Ratios and their corresponding resolutions

| Aspect Ratio | Resolution |
|--------------|------------|
| 1:1          | 512 x 512  |
| 3:4          | 416 x 576  |
| 4:3          | 576 x 416  |
| 9:16         | 384 x 672  |
| 16:9         | 672 x 384  |

### Resolution Ratio
We take the aspect ratio, ie `1:1` and get its resolution `512px x 512px` then multiply the resolution by the Ratio, 
ie `2` which results in the final resolution of `1024px x 1024px`.

| Resolution   | Ratio | Use-case                                                          |
|--------------|-------|-------------------------------------------------------------------|
| small (512)  | 1     | great for small latents and initial images for hiresfix workflows |
| medium (1024 | 2     | good for standard renders and works well for SDXL 1.0             |
| large (2048) | 4     | I don't recommend using this unless you know what you are doing   |

## Taco Animated Image Loader

Allows you to input an animated image `(must be supported by PIL)` and breaks it up into a batch of the individual 
frames.

### Example Workflow

![TAIL Workflow]()

![TAIL Gif]()

## Taco Img2Img Animated Loader

Allows you to take a single image and generate a batch of images to be processed for gif creation, I like to use this 
to spice up a still.

### Example Workflow

![TIAL Workflow]()

![TAIL Gif]()

## Taco GIf Maker

Takes an input of **IMAGE** and will combine the input into a gif at the desired frame rate, see the above examples for 
Gif Maker usage.