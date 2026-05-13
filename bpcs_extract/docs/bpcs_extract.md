# Lab: Giấu và tách tin trong video bằng BPCS

## 1. Mục đích

Bài thực hành nhằm giúp sinh viên hiểu và áp dụng kỹ thuật giấu và tách tin trong video sử dụng phương pháp mặt phẳng bit BPCS (Bit-Plane Complexity Segmentation).

Thông qua bài lab, sinh viên sẽ:

- Xem thông số kỹ thuật của file video.
- Dùng `ffmpeg` để tách video thành các khung hình.
- Dùng `ffmpeg` để trích xuất âm thanh từ video.
- Chỉnh sửa chương trình `encode.py` để giấu thông tin vào một khung hình.
- Tái tạo video mới có chứa thông tin mật.
- Tách khung hình từ video đã giấu tin.
- Chỉnh sửa chương trình `decode.py` để trích xuất lại thông tin mật.

Lab này không có script chạy tự động toàn bộ. Sinh viên phải thực hiện từng nhiệm vụ để hiểu luồng giấu/tách tin.

## 2. Yêu cầu đối với sinh viên

Để thực hiện bài lab, sinh viên cần tìm hiểu:

1. Lý thuyết về giấu và tách tin trong video bằng BPCS.
2. Cách tách video thành frame và ghép frame lại thành video.
3. Cách chọn frame, bit plane, block và ngưỡng độ phức tạp.
4. Cơ bản về Python để đọc, hiểu và chỉnh sửa code giấu/tách tin.
5. Cơ bản về `ffmpeg`.

## 3. Cấu hình bài lab

Bài lab gồm 1 container.

Khi bắt đầu, thư mục làm việc của sinh viên có 3 file:

```text
video.mp4
encode.py
decode.py
```

Trong container đã có sẵn:

- `ffmpeg`
- Python 3
- OpenCV Python
- NumPy

## 4. Chuẩn bị môi trường

Yêu cầu:

- Máy ảo Labtainer.
- Máy ảo có Docker hoạt động.
- Lab đã được import vào Labtainer.

Nếu bài lab được phát hành dạng IModule, sinh viên tải bằng lệnh tương tự:

```bash
imodule https://github.com/<username>/<repo>/releases/download/latest/bpcs_extract.tar
```

Khởi tạo bài lab:

```bash
labtainer bpcs_extract
```

Khi Labtainer yêu cầu email, sinh viên nhập email hoặc mã sinh viên theo yêu cầu của giảng viên.

## 5. Các nhiệm vụ cần thực hiện

### Task 1: Xem thông số kỹ thuật của file video

Mục tiêu: xác định thông số kỹ thuật của video như độ dài, bitrate, định dạng, kích thước khung hình, fps và thông tin audio.

Thực hiện và lưu kết quả vào file để checkwork kiểm tra:

```bash
ffmpeg -hide_banner -i video.mp4 2> video_info.txt
cat video_info.txt
```

Sinh viên cần ghi lại trong báo cáo:

- Duration
- Bitrate
- Độ phân giải video
- FPS
- Codec video
- Codec audio

### Task 2: Tách video thành các khung hình và âm thanh

Mục tiêu: phân tách video thành các ảnh frame liên tiếp để có thể áp dụng BPCS lên một frame cụ thể.

Tạo thư mục lưu frame:

```bash
mkdir frames
```

Trích xuất frame:

```bash
ffmpeg -i video.mp4 frames/frame_%04d.png
```

Trích xuất âm thanh:

```bash
ffmpeg -hide_banner -i video.mp4 -q:a 0 -map a audio.mp3
```

Sau khi thực hiện thành công:

- Thư mục `frames` chứa các ảnh `.png`.
- File `audio.mp3` chứa âm thanh tách từ video gốc.

Kiểm tra số frame:

```bash
ls frames | wc -l
```

### Task 3: Thực hiện giấu tin

Mục tiêu: áp dụng kỹ thuật BPCS lên một frame để giấu thông điệp bí mật, sau đó tái tạo lại video stego.

Mở file `encode.py`:

```bash
nano encode.py
```

Các biến cần chú ý:

```python
FRAMES_DIR = "frames"
AUDIO_FILE = "audio.mp3"
OUTPUT_VIDEO = "output.avi"
TARGET_FRAME_INDEX = 100
SECRET_DATA = "..."
FPS = 30
POSITION_FILE = "position.txt"
BIT_PLANE = 0
ALPHA_THRESHOLD = 0.35
```

Ý nghĩa:

- `FRAMES_DIR`: thư mục chứa frame tách từ video gốc.
- `AUDIO_FILE`: file âm thanh đã tách từ video gốc.
- `OUTPUT_VIDEO`: video đầu ra sau khi giấu tin.
- `TARGET_FRAME_INDEX`: khung hình muốn giấu tin.
- `SECRET_DATA`: thông điệp bí mật cần giấu.
- `FPS`: phải khớp với fps đã xem ở Task 1.
- `POSITION_FILE`: file lưu vị trí các block đã dùng để giấu tin.
- `BIT_PLANE`: mặt phẳng bit dùng để giấu tin.
- `ALPHA_THRESHOLD`: ngưỡng độ phức tạp BPCS.

Sau khi chỉnh sửa, chạy:

```bash
python3 encode.py
```

Nếu thành công, chương trình tạo:

```text
position.txt
output.avi
```

`position.txt` chứa thông tin vị trí block đã dùng để nhúng bit bí mật. File này cần thiết cho quá trình tách tin.

### Task 4: Thực hiện tách tin

Mục tiêu: trích xuất lại thông điệp bí mật từ video đã giấu tin.

Tạo thư mục chứa frame của video stego:

```bash
mkdir extract_frames
```

Tách frame từ video đã giấu tin:

```bash
ffmpeg -hide_banner -i output.avi extract_frames/frame_%04d.png
```

So sánh số frame trước và sau khi giấu:

```bash
ls frames | wc -l
ls extract_frames | wc -l
```

Mở file `decode.py`:

```bash
nano decode.py
```

Các biến cần chú ý:

```python
EXTRACT_FRAMES_DIR = "extract_frames"
TARGET_FRAME_INDEX = 100
POSITION_FILE = "position.txt"
```

Trong một số trường hợp, số thứ tự frame sau khi xuất video có thể lệch so với frame ban đầu. Ví dụ khi giấu ở frame 100 nhưng trích xuất từ `output.avi` cần đọc frame 101, sinh viên phải sửa:

```python
TARGET_FRAME_INDEX = 101
```

Chạy chương trình tách tin:

```bash
python3 decode.py
```

Nếu thành công, chương trình in ra thông điệp bí mật và tạo:

```text
recovered_secret.txt
```

### Task 5: Kiểm tra kết quả

Kiểm tra thông điệp trích xuất có giống thông điệp ban đầu trong `encode.py` hay không.

Nếu không giống, sinh viên cần kiểm tra:

1. Có dùng đúng `position.txt` không?
2. Có dùng đúng `TARGET_FRAME_INDEX` không?
3. `FPS` khi ghép video có đúng với video gốc không?
4. Video có được xuất bằng codec ít mất dữ liệu không?
5. Có tách lại frame từ đúng file `output.avi` không?

## 6. Checkwork không làm mất container

Trong bài lab này có sẵn một lệnh `checkwork` chạy ngay bên trong container. Lệnh này chỉ kiểm tra file kết quả trong thư mục hiện tại, không dừng container và không đóng terminal.

Sau khi hoàn thành các task, chạy trong terminal của lab:

```bash
checkwork
```

Lệnh này kiểm tra 5 nhóm kết quả:

1. `video_info.txt` đã được tạo từ lệnh xem thông tin video.
2. Thư mục `frames` có đủ frame ảnh.
3. File `audio.mp3` đã được tách.
4. `position.txt` và `output.avi` đã được tạo sau khi chạy `encode.py`.
5. `extract_frames` và `recovered_secret.txt` hợp lệ sau khi chạy `decode.py`.

Nếu hoàn thành đúng, kết quả cuối sẽ có:

```text
BPCS_LOCAL_CHECKWORK_PASS
```

Lưu ý: lệnh `checkwork bpcs_extract` ở terminal ngoài Labtainer là checkwork chuẩn của Labtainer, có thể thu bài và tác động đến trạng thái container theo cơ chế của Labtainer. Nếu chỉ muốn tự kiểm tra khi đang làm bài, hãy dùng lệnh `checkwork` bên trong container.

## 7. Kết thúc bài lab

Trên terminal đầu tiên, kết thúc lab:

```bash
stoplab bpcs_extract
```

Khi bài lab kết thúc, Labtainer tạo một file zip kết quả và hiển thị đường dẫn lưu file.

## 8. Khởi động lại bài lab

Nếu cần thực hiện lại bài lab:

```bash
labtainer -r bpcs_extract
```

## 9. Câu hỏi báo cáo

Sinh viên trả lời các câu hỏi sau:

1. Video gốc có độ phân giải, fps và codec là gì?
2. Vì sao cần tách video thành các frame trước khi giấu tin?
3. BPCS dùng độ phức tạp block để chọn vùng nhúng như thế nào?
4. Vai trò của file `position.txt` là gì?
5. Vì sao `TARGET_FRAME_INDEX` trong `decode.py` có thể cần chỉnh lệch so với `encode.py`?
6. Nếu dùng codec nén mất dữ liệu, quá trình tách tin có thể bị ảnh hưởng như thế nào?

## 10. Yêu cầu nộp

Sinh viên cần có các file kết quả:

```text
video_info.txt
frames/
audio.mp3
position.txt
output.avi
extract_frames/
recovered_secret.txt
```

Và báo cáo ngắn mô tả quá trình thực hiện, lỗi gặp phải nếu có, thông điệp ban đầu và thông điệp tách được.
