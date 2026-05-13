# bpcs_extract

Labtainer lab for video steganography with BPCS bit-plane complexity embedding and extraction.

## Install

From the Labtainer student VM:

~~~bash
cd /home/student/labtainer/trunk/scripts/labtainer-student
imodule https://github.com/<github-user>/<repo>/raw/main/bpcs_extract.tar.gz
labtainer bpcs_extract
~~~

## Student Workflow

The lab guides students through:

1. Inspecting technical metadata of video.mp4.
2. Extracting video frames and audio with ffmpeg.
3. Hiding a secret message using encode.py.
4. Extracting frames from the stego video.
5. Recovering the hidden message with decode.py.

## Notes

The packaged lab includes the Labtainer source folder and bpcs_extract.tar.gz for direct installation with imodule.
