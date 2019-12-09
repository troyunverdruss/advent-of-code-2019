from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw
from pygifsicle import gifsicle

from helpers import read_raw_entries


def part1(wide: int, tall: int, input_bits: List[int]) -> int:
    # This will hold the result of each layer's analysis
    # Entries are tuples: (count of 0s, count of 1s * count of 2s)
    # So layer like this: 0 0 1 1 1 2 => (2, 3*1=3)
    layer_analysis: List[Tuple[int, int]] = []

    # We're going to go through all the bits, but we're going to do it in blocks
    # based on the calculated offset. Goes by pixels per layer, like so for a 3x2 image:
    # layer * offset
    # 0*0, 1*3*2, 2*3*2 => 0, 6, 12 ...
    for offset in range(0, len(input_bits), wide * tall):
        # A little wasteful, but grab the whole layer
        layer = input_bits[offset: wide * tall + offset]
        # Stuff it into counter
        counts = Counter(layer)
        # Store the layer analysis result:
        # (count of 0s, count of 1s * count of 2s)
        layer_analysis.append((counts[0], counts[1] * counts[2]))

    # Iterate over all the layer analysis data and find the entry
    # with the minimum value for 0s (position 0)
    min_entry = min(layer_analysis, key=lambda v: v[0])

    # Then return the 1s*2s values from position 1
    return min_entry[1]


# Part 2 has us read in layers into a single buffer where the first
# visible pixel (based on previous pixels being transparent) is the one
# that we should "see". Since 2 is transparent, it's the value we'll key
# from, everything starts transparent and only if a field is still transparent
# does it matter what could possibly go there. Always write the value we find
# until it is no longer transparent, then leave it be.
def part2_read_into_buffer(wide, tall, input_bits):
    buffer = defaultdict(lambda: 2)
    t = 0
    for offset in range(0, len(input_bits), wide * tall):
        t += 1
        layer = input_bits[offset: offset + wide * tall]
        for y in range(tall):
            for x in range(wide):
                if buffer[(x, y)] == 2:
                    buffer[(x, y)] = layer[y * wide + x]
        # This is only useful if you want to write images as a gif
        # Path("raw_images").mkdir()
        # write_buffer_to_image(wide, tall, buffer, f"raw_images/time_{str(t).zfill(3)}.gif")
    # This is also only for writing a gif
    # write_gif_from_images()

    return buffer


# Simple go through the data and print it out row by row
# with spaces and # to delineate black and white
def print_buffer_to_console(wide, tall, buffer):
    # 0: Black, 1: White
    color_lookup = {0: " ", 1: "#"}

    for y in range(tall):
        for x in range(wide):
            print(color_lookup[buffer[(x, y)]], end="")
            print(" ", end="")
        print("")


# For bonus credit, write out a real image file with the same data
def write_buffer_to_image(wide: int, tall: int, buffer: Dict[Tuple[int, int], int], img_name: str):
    color_lookup = {0: "black", 1: "white", 2: None}

    # DPI is the wrong term, but used here to magnify from pixels to larger rects
    dpi = 50
    image = Image.new("RGBA", (wide * dpi, tall * dpi))
    image_draw = ImageDraw.Draw(image)

    # Go through all the buffer data, writing it based on the color lookup map
    # and skipping a write if the map says "transparent". Note that rect definitions
    # are *inclusive* so 10x10 rect goes from (0,0) to (9,9), not (10,10). That's why
    # there's a "-1" on each rect definition
    for y in range(tall):
        for x in range(wide):
            color = color_lookup[buffer[(x, y)]]
            if color:
                rect = (x * dpi, y * dpi, x * dpi + dpi - 1, y * dpi + dpi - 1)
                # print(f"printing {color} to {rect}")
                image_draw.rectangle(rect, fill=color)

    # # Pixel debugging
    # for x in range(wide * dpi):
    #     if x % 2 == 0:
    #         image_draw.rectangle((x, 0, x, 0), fill="cyan")
    # for y in range(tall * dpi):
    #     if y % 2 == 0:
    #         image_draw.rectangle((0, y, 0, y), fill="cyan")
    image.save(img_name)


# This tries to assemble all the raw gifs into an animated one
def write_gif_from_images():
    images = sorted(map(str, Path("raw_images/").glob("*.gif")))
    gifsicle(
        sources=list(images),
        destination="combined.gif",
        optimize=True,
        colors=256,
        options=[f"--delay={10}"]
    )


if __name__ == "__main__":
    line = read_raw_entries("input08.txt")[0]
    bits = list(map(int, line))

    part1 = part1(25, 6, bits)
    print(f"Part 1: {part1}")

    part2_buffer = part2_read_into_buffer(25, 6, bits)
    print("Part 2:")

    print_buffer_to_console(25, 6, part2_buffer)

    write_buffer_to_image(25, 6, part2_buffer, "part2.png")
