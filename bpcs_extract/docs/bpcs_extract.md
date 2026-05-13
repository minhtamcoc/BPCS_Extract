# BPCS Extract

## Muc dich

Bai thuc hanh giup sinh vien thuc hien quy trinh giau va tach tin
trong video bang phuong phap BPCS bit-plane.

Sinh vien khong chay mot script tu dong toan bo. Moi buoc can duoc thuc
hien rieng de thay ro luong xu ly video, frame, audio, encode va decode.

## File ban dau

Khi mo lab, thu muc lam viec co 3 file:

```text
video.mp4
encode.py
decode.py
```

## Task 1: Xem thong tin video

```bash
ffmpeg -hide_banner -i video.mp4 2> video_info.txt
cat video_info.txt
```

Can xac dinh duration, bitrate, codec, kich thuoc khung hinh va fps.

## Task 2: Tach frame va audio

```bash
mkdir frames
ffmpeg -i video.mp4 frames/frame_%04d.png
ffmpeg -hide_banner -i video.mp4 -q:a 0 -map a audio.mp3
```

## Task 3: Giau tin

Mo file encode.py:

```bash
nano encode.py
```

Kiem tra cac bien quan trong:

```text
FRAMES_DIR
AUDIO_FILE
OUTPUT_VIDEO
TARGET_FRAME_INDEX
SECRET_DATA
FPS
POSITION_FILE
BIT_PLANE
ALPHA_THRESHOLD
```

Chay chuong trinh:

```bash
python3 encode.py
```

Ket qua can co:

```text
position.txt
output.avi
```

## Task 4: Tach tin

Tach frame tu video da giau tin:

```bash
mkdir extract_frames
ffmpeg -hide_banner -i output.avi extract_frames/frame_%04d.png
```

Mo file decode.py:

```bash
nano decode.py
```

Neu can, sua TARGET_FRAME_INDEX tu 100 thanh 101 do su lech frame sau
khi xuat video.

Chay:

```bash
python3 decode.py
```

Ket qua can co:

```text
recovered_secret.txt
```

## Checkwork

Tu terminal Labtainer ben ngoai container:

```bash
checkwork
```

Lab co 5 muc cham:

```text
cw1: da luu thong tin video vao video_info.txt
cw2: da tach frame bang mau ten frames/frame_%04d.png
cw3: da tach audio thanh audio.mp3
cw4: da tao position.txt khi chay encode.py
cw5: da khoi phuc thong diep trong recovered_secret.txt
```

## Stoplab

Ket thuc bai lab:

```bash
stoplab bpcs_extract
```

Labtainer se tao file .lab va file diem trong thu muc ket qua cua lab.
