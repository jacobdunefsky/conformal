# conformal
A conformal mapper written in Python; a small exercise from 2018.

## Installing
1. Install numpy
2. Install pygame
3. Download the repository to wherever you'd like

## Usage
Run `python conformal.py IMAGE [-t]` where `IMAGE` is a path to the image you'd like to transform and the `-t` option causes the resulting image to be tiled. If no arguments are provided, `conformal` will default to using the image `think.png` provided in the same directory as `conformal.py`.

On the command line, you determine the transformation by entering any valid Python expression with the variable `z`. You have access to the `cmath` and `numpy` libraries, so you can really let your imagination run wild. An example transformation is `1/z if not z == 0 else 0`, which denotes the reciprocal transformation (while accounting for a possible division by zero). Another example is `cmath.sqrt(z)`. The sky really is the limit.

Clicking on the image displayed will switch between the original image and the transformed image, allowing you to better understand what the transformation is doing.

To quit, simply type `quit` on the command line in place of an actual expression.
