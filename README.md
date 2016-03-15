This tool generates a raytraced video (or rather, a sequence of frames) of a 3x3x3 Rubik's cube, using POV-Ray, given a sequence of moves. It needs Python3 with numpy, and POV-ray.

#Usage
Run `r.py` in an empty directory (this is preferable since it creates several files). It reads a sequence of moves in Singmaster notation from standard input, and produces POV-Ray source files, and a render script which calls POV-Ray. The file `cube_setup_scene.inc` needs to be available in the same directory for the script to run.

## Singmaster notation
Currently supports FBUDLR, corresponding two-layer moves (both f,b,etc and Fw,Bw,etc), whole cube rotations (x,y,z), and inverses of all the above. Also supports 180-degree rotations (F2, f2, Fw2, x2, etc).
