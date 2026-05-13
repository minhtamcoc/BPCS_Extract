# Write-up bài lab: Giấu và tách tin trong video bằng BPCS

## 1. Thông tin chung

Tên bài lab:

```text
bpcs_extract
```

Chủ đề:

```text
Giấu tin và tách tin trong video bằng phương pháp BPCS
```

Phương pháp sử dụng:

```text
BPCS - Bit-Plane Complexity Segmentation
```

Môi trường triển khai:

```text
Labtainer
Docker container Ubuntu
Python 3
OpenCV
NumPy
ffmpeg
```

## 2. Mục đích

Bài thực hành nhằm giúp sinh viên hiểu và áp dụng kỹ thuật giấu tin trong video bằng phương pháp mặt phẳng bit BPCS. Thông qua bài lab, sinh viên thực hiện đầy đủ quy trình từ phân tích video gốc, tách video thành các khung hình, trích xuất âm thanh, giấu thông tin vào một khung hình, tái tạo video mới, sau đó tách lại thông tin đã giấu từ video stego.

Bài lab không được thiết kế theo kiểu chạy một script duy nhất để ra kết quả. Thay vào đó, sinh viên phải thực hiện từng bước thủ công bằng `ffmpeg`, chỉnh sửa các biến cấu hình trong `encode.py` và `decode.py`, sau đó tự kiểm tra kết quả trích xuất. Cách làm này giúp sinh viên hiểu rõ hơn mối liên hệ giữa video, frame, bit plane, block BPCS và quá trình nhúng/tách tin.

## 3. Kiến thức sinh viên cần chuẩn bị

Để hoàn thành bài lab, sinh viên cần nắm các kiến thức sau:

1. Khái niệm cơ bản về steganography.
2. Cấu trúc video gồm chuỗi khung hình và luồng âm thanh.
3. Cách sử dụng `ffmpeg` để xem thông tin, tách frame và tách audio.
4. Biểu diễn pixel bằng các mặt phẳng bit.
5. Độ phức tạp của block trong BPCS.
6. Cơ bản về Python, OpenCV và NumPy.

## 4. Cấu hình bài lab

Bài lab gồm một container duy nhất. Khi sinh viên khởi động lab, thư mục làm việc ban đầu có 3 file chính:

```text
video.mp4
encode.py
decode.py
```

Ý nghĩa các file:

- `video.mp4`: video gốc dùng làm môi trường chứa tin.
- `encode.py`: chương trình giấu thông điệp vào một frame của video.
- `decode.py`: chương trình tách lại thông điệp từ video đã giấu tin.

Trong quá trình làm bài, sinh viên sẽ tạo thêm các file/thư mục:

```text
frames/
audio.mp3
position.txt
output.avi
extract_frames/
recovered_secret.txt
```

## 5. Chuẩn bị môi trường

Khởi động bài lab:

```bash
labtainer bpcs_extract
```

Nếu cần khởi động lại bài lab:

```bash
labtainer -r bpcs_extract
```

Kết thúc bài lab:

```bash
stoplab bpcs_extract
```

Kiểm tra kết quả bằng checkwork:

```bash
checkwork bpcs_extract
```

## 6. Cơ sở lý thuyết BPCS

Mỗi pixel 8 bit có thể biểu diễn dưới dạng:

```text
pixel = b7 b6 b5 b4 b3 b2 b1 b0
```

Trong đó:

- `b7` là bit quan trọng nhất.
- `b0` là bit ít quan trọng nhất.

Phương pháp BPCS khai thác các mặt phẳng bit của ảnh hoặc frame video. Thay vì chỉ thay đổi bit thấp theo kiểu LSB tuần tự, BPCS chọn các block có độ phức tạp cao để nhúng dữ liệu. Các block phức tạp thường giống nhiễu hoặc texture, nên việc thay đổi chúng ít bị mắt người phát hiện hơn.

Với một block nhị phân kích thước `n x n`, độ phức tạp được tính theo công thức:

```text
alpha = transitions / (2 * n * (n - 1))
```

Trong đó:

- `transitions` là số lần chuyển đổi giữa hai bit kề nhau theo chiều ngang và chiều dọc.
- `2 * n * (n - 1)` là số chuyển tiếp tối đa.
- `alpha` nằm trong khoảng từ 0 đến 1.

Trong bài lab, block mặc định có kích thước:

```text
8 x 8
```

Vì vậy:

```text
max_transitions = 2 * 8 * 7 = 112
```

Một block được chọn để giấu tin nếu:

```text
alpha >= ALPHA_THRESHOLD
```

## 7. Quy trình thực hiện bài lab

### Task 1: Xem thông số kỹ thuật của video

Mục tiêu của task này là xác định các thông số kỹ thuật của video gốc như thời lượng, bitrate, độ phân giải, fps, codec video và codec audio.

Lệnh thực hiện và lưu thông tin vào file để checkwork kiểm tra:

```bash
ffmpeg -hide_banner -i video.mp4 2> video_info.txt
cat video_info.txt
```

Sinh viên cần ghi lại các thông tin:

- Duration
- Bitrate
- Resolution
- FPS
- Video codec
- Audio codec

Ví dụ kết quả mong đợi có dạng:

```text
Duration: 00:00:05.xx
Video: h264, 640x360, 30 fps
Audio: aac, 44100 Hz
```

Thông tin FPS rất quan trọng vì khi tái tạo video mới, biến `FPS` trong `encode.py` cần khớp với video gốc.

### Task 2: Tách video thành frame và audio

Tạo thư mục chứa frame:

```bash
mkdir frames
```

Tách video thành các khung hình:

```bash
ffmpeg -i video.mp4 frames/frame_%04d.png
```

Sau lệnh này, các frame sẽ được lưu với tên:

```text
frames/frame_0001.png
frames/frame_0002.png
frames/frame_0003.png
...
```

Tách âm thanh từ video:

```bash
ffmpeg -hide_banner -i video.mp4 -q:a 0 -map a audio.mp3
```

Kiểm tra số lượng frame:

```bash
ls frames | wc -l
```

Kết quả của task này:

```text
frames/
audio.mp3
```

### Task 3: Giấu tin vào video

Mở file `encode.py`:

```bash
nano encode.py
```

Các biến quan trọng trong `encode.py`:

```python
FRAMES_DIR = "frames"
AUDIO_FILE = "audio.mp3"
OUTPUT_VIDEO = "output.avi"
TARGET_FRAME_INDEX = 100
SECRET_DATA = "BPCS video steganography"
FPS = 30
POSITION_FILE = "position.txt"
BLOCK_SIZE = 8
BIT_PLANE = 0
ALPHA_THRESHOLD = 0.35
CHANNEL = 0
```

Ý nghĩa:

- `FRAMES_DIR`: thư mục chứa frame tách từ video gốc.
- `AUDIO_FILE`: file audio đã tách từ video gốc.
- `OUTPUT_VIDEO`: video đầu ra sau khi giấu tin.
- `TARGET_FRAME_INDEX`: frame được chọn để giấu thông điệp.
- `SECRET_DATA`: thông điệp cần giấu.
- `FPS`: tốc độ khung hình khi ghép video lại.
- `POSITION_FILE`: file lưu vị trí các block đã nhúng.
- `BLOCK_SIZE`: kích thước block BPCS.
- `BIT_PLANE`: mặt phẳng bit được dùng để nhúng.
- `ALPHA_THRESHOLD`: ngưỡng độ phức tạp BPCS.
- `CHANNEL`: kênh màu được chọn trong ảnh BGR.

Sau khi kiểm tra/chỉnh sửa cấu hình, chạy:

```bash
python3 encode.py
```

Nếu chạy thành công, chương trình tạo ra:

```text
position.txt
output.avi
```

Trong đó:

- `position.txt` lưu metadata phục vụ quá trình tách tin.
- `output.avi` là video đã được giấu thông điệp.

Khi thành công, terminal sẽ có dòng:

```text
POSITION_FILE_WRITTEN position.txt
```

Đây cũng là một mốc được dùng trong checkwork.

## 8. Cơ chế hoạt động của encode.py

Chương trình `encode.py` thực hiện các bước chính:

1. Đọc thông điệp trong biến `SECRET_DATA`.
2. Chuyển thông điệp thành chuỗi bit.
3. Thêm header 4 byte để lưu độ dài thông điệp.
4. Chia chuỗi bit thành các block `8x8`.
5. Đọc frame cần nhúng từ thư mục `frames`.
6. Lấy một kênh màu và một mặt phẳng bit.
7. Duyệt các block trong mặt phẳng bit.
8. Tính độ phức tạp `alpha` của từng block.
9. Chỉ chọn block có `alpha >= ALPHA_THRESHOLD`.
10. Thay block phức tạp bằng block dữ liệu bí mật.
11. Nếu block dữ liệu bí mật có độ phức tạp thấp, chương trình dùng phép conjugation với mẫu bàn cờ.
12. Lưu vị trí nhúng vào `position.txt`.
13. Ghi frame đã thay đổi trở lại thư mục `frames`.
14. Dùng `ffmpeg` ghép lại frame và audio thành `output.avi`.

Trong bài lab này, video đầu ra dùng codec `ffv1`, là codec lossless. Điều này giúp dữ liệu giấu trong bit plane không bị phá hỏng khi tái tạo video.

## 9. Task 4: Tách tin từ video đã giấu

Tạo thư mục chứa frame của video stego:

```bash
mkdir extract_frames
```

Tách frame từ video đã giấu tin:

```bash
ffmpeg -hide_banner -i output.avi extract_frames/frame_%04d.png
```

So sánh số lượng frame trước và sau khi giấu:

```bash
ls frames | wc -l
ls extract_frames | wc -l
```

Mở file `decode.py`:

```bash
nano decode.py
```

Các biến quan trọng:

```python
EXTRACT_FRAMES_DIR = "extract_frames"
TARGET_FRAME_INDEX = 100
POSITION_FILE = "position.txt"
RECOVERED_FILE = "recovered_secret.txt"
```

Do cách `ffmpeg` đặt tên frame bắt đầu từ `frame_0001.png`, trong bài lab này frame được nhúng ở chỉ số `100` trong `encode.py` sẽ tương ứng với:

```text
extract_frames/frame_0101.png
```

Vì vậy sinh viên cần sửa:

```python
TARGET_FRAME_INDEX = 100
```

thành:

```python
TARGET_FRAME_INDEX = 101
```

Sau đó chạy:

```bash
python3 decode.py
```

Nếu thành công, chương trình in ra:

```text
Recovered secret:
BPCS video steganography
BPCS_DECODE_SUCCESS recovered_secret.txt
```

Đồng thời tạo file:

```text
recovered_secret.txt
```

## 10. Cơ chế hoạt động của decode.py

Chương trình `decode.py` thực hiện các bước:

1. Đọc metadata từ `position.txt`.
2. Xác định block size, bit plane, kênh màu và danh sách vị trí đã nhúng.
3. Đọc frame tương ứng trong thư mục `extract_frames`.
4. Lấy mặt phẳng bit đã dùng khi nhúng.
5. Đọc lại các block theo danh sách vị trí trong `position.txt`.
6. Nếu block nào đã conjugate khi nhúng, chương trình đảo lại bằng mẫu bàn cờ.
7. Ghép các bit thu được thành byte.
8. Đọc 4 byte đầu để biết độ dài thông điệp.
9. Trích xuất thông điệp và ghi vào `recovered_secret.txt`.

File `position.txt` đóng vai trò như khóa phụ trợ. Nếu mất file này, chương trình không biết cần đọc block nào để khôi phục dữ liệu.

## 11. Checkwork

Bài lab hỗ trợ hai kiểu checkwork.

Kiểu thứ nhất là checkwork chạy ngay bên trong container:

```bash
checkwork
```

Kiểu này không dừng container, không đóng terminal, chỉ kiểm tra các file kết quả hiện có trong thư mục `/home/student`.

Nó kiểm tra 5 nhóm kết quả:

1. `video_info.txt` đã được tạo từ lệnh xem thông tin video.
2. `frames/` đã có đủ frame ảnh.
3. `audio.mp3` đã được trích xuất.
4. `position.txt` và `output.avi` đã được tạo sau khi chạy `encode.py`.
5. `extract_frames/` và `recovered_secret.txt` hợp lệ sau khi chạy `decode.py`.

Nếu hoàn thành đúng, terminal sẽ in:

```text
BPCS_LOCAL_CHECKWORK_PASS
```

Kiểu thứ hai là checkwork chuẩn của Labtainer, chạy ở terminal ngoài container:

```bash
checkwork bpcs_extract
```

Kiểu này phục vụ chấm điểm/thu kết quả theo cơ chế Labtainer, nên có thể tác động tới trạng thái container. Nếu sinh viên chỉ muốn tự kiểm tra trong lúc làm bài, nên dùng `checkwork` bên trong container.

Bài lab có cấu hình checkwork chuẩn trong:

```text
instr_config/results.config
instr_config/goals.config
```

Checkwork chuẩn kiểm tra các dấu mốc:

1. Sinh viên đã lưu thông tin video vào `video_info.txt`.
2. Sinh viên đã tách frame bằng `ffmpeg`.
3. Sinh viên đã tách audio thành `audio.mp3`.
4. Sinh viên đã chạy giấu tin thành công:

```text
POSITION_FILE_WRITTEN
```

5. Sinh viên đã tách tin thành công:

```text
BPCS_DECODE_SUCCESS
```

Sau khi làm xong các task, sinh viên chạy ở terminal ngoài container:

```bash
checkwork bpcs_extract
```

Nếu cả hai dấu mốc đều được ghi nhận, bài lab được xem là hoàn thành.

## 12. Các lỗi thường gặp

### Lỗi 1: Không tìm thấy frame cần nhúng

Nguyên nhân:

- Chưa chạy lệnh tách frame.
- Tên thư mục frame sai.
- `TARGET_FRAME_INDEX` lớn hơn số frame hiện có.

Cách kiểm tra:

```bash
ls frames | wc -l
```

### Lỗi 2: Không tìm thấy audio.mp3

Nguyên nhân:

- Chưa chạy lệnh tách audio.

Cách khắc phục:

```bash
ffmpeg -hide_banner -i video.mp4 -q:a 0 -map a audio.mp3
```

### Lỗi 3: Decode ra lỗi hoặc không đúng thông điệp

Nguyên nhân thường gặp:

- `TARGET_FRAME_INDEX` trong `decode.py` chưa chỉnh từ `100` sang `101`.
- Tách frame từ sai video.
- File `position.txt` bị thiếu hoặc không đúng.

Cách kiểm tra:

```bash
ls frames | wc -l
ls extract_frames | wc -l
```

### Lỗi 4: Không đủ block phức tạp để giấu tin

Nguyên nhân:

- `ALPHA_THRESHOLD` quá cao.
- Frame được chọn quá ít texture.
- Thông điệp quá dài.

Cách khắc phục:

- Giảm `ALPHA_THRESHOLD`.
- Chọn frame khác.
- Giảm độ dài `SECRET_DATA`.

## 13. Câu hỏi báo cáo

Sinh viên cần trả lời:

1. Video gốc có độ phân giải, fps, codec video và codec audio là gì?
2. Vì sao cần tách video thành frame trước khi giấu tin?
3. BPCS chọn block nhúng dựa trên tiêu chí nào?
4. Vai trò của `position.txt` trong quá trình tách tin là gì?
5. Vì sao `TARGET_FRAME_INDEX` trong `decode.py` cần sửa từ `100` thành `101`?
6. Nếu dùng codec nén mất dữ liệu thay vì `ffv1`, thông điệp có thể bị ảnh hưởng như thế nào?
7. Nếu tăng `ALPHA_THRESHOLD`, dung lượng giấu tin thay đổi ra sao?

## 14. Kết luận

Thông qua bài lab, sinh viên nắm được quy trình cơ bản của giấu tin trong video bằng BPCS. Video được tách thành các frame, thông điệp được chuyển thành bit và nhúng vào các block có độ phức tạp cao trong một mặt phẳng bit của frame. Sau đó video được tái tạo lại và thông điệp được tách ra dựa trên file vị trí `position.txt`.

Bài lab cũng cho thấy một số vấn đề thực tế khi giấu tin trong video, như việc đồng bộ chỉ số frame, lựa chọn codec không mất dữ liệu, lựa chọn ngưỡng độ phức tạp và vai trò của metadata trong quá trình tách tin.

## 15. Tóm tắt lệnh thực hiện

```bash
ffmpeg -hide_banner -i video.mp4 2> video_info.txt
cat video_info.txt

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

Trong `decode.py`, cần sửa:

```python
TARGET_FRAME_INDEX = 101
```

Kết quả đúng:

```text
Recovered secret:
BPCS video steganography
```
