# bpcs_extract

Labtainer lab for video steganography using a BPCS bit-plane method.

This version is intentionally scenario-based. It does not provide a single script that completes the lab automatically. Students must run `ffmpeg`, inspect/edit `encode.py`, run the encoder, extract frames from the stego video, inspect/edit `decode.py`, and recover the secret message.

## Student-visible files

Inside the lab container, the student starts with only:

```text
video.mp4
encode.py
decode.py
```

Generated during the lab:

```text
frames/
audio.mp3
position.txt
output.avi
extract_frames/
recovered_secret.txt
```

## Docker base image

The Dockerfile follows the same style as the existing `bpcs_video_hide_practice` lab on the VM:

```text
FROM ubuntu:20.04
```

It installs `ffmpeg`, `nano`, Python 3, OpenCV and NumPy during build.

## Install

Copy this folder into:

```bash
/home/student/labtainer/trunk/labs/bpcs_extract
```

Build:

```bash
cd /home/student/labtainer/trunk/scripts/labtainer-student
python3 bin/rebuild.py bpcs_extract
```

Run as student:

```bash
labtainer bpcs_extract
```

## Expected student workflow

```bash
ffmpeg -hide_banner -i video.mp4
mkdir frames
ffmpeg -i video.mp4 frames/frame_%04d.png
ffmpeg -hide_banner -i video.mp4 -q:a 0 -map a audio.mp3
nano encode.py
python3 encode.py
mkdir extract_frames
ffmpeg -hide_banner -i output.avi extract_frames/frame_%04d.png
nano decode.py
python3 decode.py
```

If decoding fails, students compare frame counts:

```bash
ls frames | wc -l
ls extract_frames | wc -l
```

Then adjust `TARGET_FRAME_INDEX` in `decode.py`.
