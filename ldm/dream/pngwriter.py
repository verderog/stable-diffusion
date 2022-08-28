"""
Two helper classes for dealing with PNG images and their path names.
PngWriter -- Converts Images generated by T2I into PNGs, finds
             appropriate names for them, and writes prompt metadata
             into the PNG. Intended to be subclassable in order to
             create more complex naming schemes, including using the
             prompt for file/directory names.
PromptFormatter -- Utility for converting a Namespace of prompt parameters
             back into a formatted prompt string with command-line switches.
"""
import os
import re
from math import sqrt, floor, ceil
from PIL import Image, PngImagePlugin

# -------------------image generation utils-----
class PngWriter:
    def __init__(self, outdir, prompt=None, batch_size=1):
        self.outdir = outdir
        self.batch_size = batch_size
        self.prompt = prompt
        self.filepath = None
        self.files_written = []
        os.makedirs(outdir, exist_ok=True)

    def write_image(self, image, seed):
        self.filepath = self.unique_filename(
            seed, self.filepath
        )   # will increment name in some sensible way
        try:
            prompt = f'{self.prompt} -S{seed}'
            self.save_image_and_prompt_to_png(image, prompt, self.filepath)
        except IOError as e:
            print(e)
        self.files_written.append([self.filepath, seed])

    def unique_filename(self, seed, previouspath=None):
        revision = 1

        if previouspath is None:
            # sort reverse alphabetically until we find max+1
            dirlist = sorted(os.listdir(self.outdir), reverse=True)
            # find the first filename that matches our pattern or return 000000.0.png
            filename = next(
                (f for f in dirlist if re.match('^(\d+)\..*\.png', f)),
                '0000000.0.png',
            )
            basecount = int(filename.split('.', 1)[0])
            basecount += 1
            if self.batch_size > 1:
                filename = f'{basecount:06}.{seed}.01.png'
            else:
                filename = f'{basecount:06}.{seed}.png'
            return os.path.join(self.outdir, filename)

        else:
            basename = os.path.basename(previouspath)
            x = re.match('^(\d+)\..*\.png', basename)
            if not x:
                return self.unique_filename(seed, previouspath)

            basecount = int(x.groups()[0])
            series = 0
            finished = False
            while not finished:
                series += 1
                filename = f'{basecount:06}.{seed}.png'
                if self.batch_size > 1 or os.path.exists(
                    os.path.join(self.outdir, filename)
                ):
                    filename = f'{basecount:06}.{seed}.{series:02}.png'
                finished = not os.path.exists(
                    os.path.join(self.outdir, filename)
                )
            return os.path.join(self.outdir, filename)

    def save_image_and_prompt_to_png(self, image, prompt, path):
        info = PngImagePlugin.PngInfo()
        info.add_text('Dream', prompt)
        image.save(path, 'PNG', pnginfo=info)

    def make_grid(self, image_list, rows=None, cols=None):
        image_cnt = len(image_list)
        if None in (rows, cols):
            rows = floor(sqrt(image_cnt))  # try to make it square
            cols = ceil(image_cnt / rows)
        width = image_list[0].width
        height = image_list[0].height

        grid_img = Image.new('RGB', (width * cols, height * rows))
        for r in range(0, rows):
            for c in range(0, cols):
                i = r * rows + c
                grid_img.paste(image_list[i], (c * width, r * height))

        return grid_img



