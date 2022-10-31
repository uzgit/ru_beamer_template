#!/usr/bin/python3

import argparse
import pathlib
import sys
import glob
from PIL import Image
import pyheif
import webp

parser = argparse.ArgumentParser()
parser.add_argument("image_filenames", nargs="+", help="path or regex for input files", type=str)
parser.add_argument("-f", "--output_format", default="webp")
parser.add_argument("-q", "--quality", default=100)
args = parser.parse_args()

pil_supported_formats = Image.registered_extensions()
print(f"Converting {args.image_filenames} to {args.output_format} with {args.quality} % quality...")

for image_filename in args.image_filenames:

    input_format = pathlib.Path(image_filename).suffix.lower()
    output_filename = image_filename.split(".")[0] + "." + args.output_format
    print(f"Converting {image_filename} (format: {input_format}) to {output_filename} ...")

    image = None
    if( input_format in [".heic"] ):
        print(f"\t{input_format} -> opening {image_filename} as heic...")
        heif_file = pyheif.read( image_filename )

        image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,            
                )

    #elif( input_format in [".webp"] ):
    #    print(f"\t{input_format} -> opening {image_filename} as webp...")
    elif( input_format in pil_supported_formats):
        print(f"\t{input_format} -> opening {image_filename} with PIL")
        image = Image.open( image_filename )

    if( image is not None ):
        print("\tgonna do things to this image now!")
        image.save(output_filename, quality=args.quality)
    else:
        print("failed to process {image_filename}")

