import json
import subprocess
from pathlib import Path

import cv2
import numpy as np


# ====== Student configuration ======
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
CHANNEL = 0  # BGR channel: 0=B, 1=G, 2=R
# ===================================


def text_to_bits(text):
    payload = text.encode("utf-8")
    length_header = len(payload).to_bytes(4, "big")
    data = length_header + payload
    bits = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def checkerboard(n):
    y, x = np.indices((n, n))
    return ((x + y) % 2).astype(np.uint8)


def block_complexity(block):
    horizontal = np.sum(block[:, :-1] != block[:, 1:])
    vertical = np.sum(block[:-1, :] != block[1:, :])
    max_transitions = 2 * block.shape[0] * (block.shape[0] - 1)
    return float(horizontal + vertical) / float(max_transitions)


def bits_to_blocks(bits, block_size):
    block_bits = block_size * block_size
    blocks = []
    for start in range(0, len(bits), block_bits):
        chunk = bits[start : start + block_bits]
        valid_bits = len(chunk)
        if len(chunk) < block_bits:
            chunk = chunk + [0] * (block_bits - len(chunk))
        blocks.append((np.array(chunk, dtype=np.uint8).reshape(block_size, block_size), valid_bits))
    return blocks


def frame_name(frame_index):
    return f"frame_{frame_index:04d}.png"


def rebuild_video():
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        f"{FRAMES_DIR}/frame_%04d.png",
    ]

    if Path(AUDIO_FILE).exists():
        cmd += ["-i", AUDIO_FILE, "-c:a", "copy", "-shortest"]

    # FFV1 is lossless, which keeps the hidden bit-plane data stable.
    cmd += ["-c:v", "ffv1", OUTPUT_VIDEO]

    print("Rebuilding video:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    frame_path = Path(FRAMES_DIR) / frame_name(TARGET_FRAME_INDEX)
    if not frame_path.exists():
        raise FileNotFoundError(
            f"Cannot find {frame_path}. Did you run: ffmpeg -i video.mp4 frames/frame_%04d.png ?"
        )

    frame = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
    if frame is None:
        raise RuntimeError(f"Cannot read frame {frame_path}")

    channel = frame[:, :, CHANNEL].copy()
    bit_plane = ((channel >> BIT_PLANE) & 1).astype(np.uint8)

    secret_bits = text_to_bits(SECRET_DATA)
    payload_blocks = bits_to_blocks(secret_bits, BLOCK_SIZE)
    board = checkerboard(BLOCK_SIZE)

    positions = []
    payload_index = 0
    height, width = bit_plane.shape

    for y in range(0, height - height % BLOCK_SIZE, BLOCK_SIZE):
        for x in range(0, width - width % BLOCK_SIZE, BLOCK_SIZE):
            if payload_index >= len(payload_blocks):
                break

            cover_block = bit_plane[y : y + BLOCK_SIZE, x : x + BLOCK_SIZE]
            if block_complexity(cover_block) < ALPHA_THRESHOLD:
                continue

            payload_block, valid_bits = payload_blocks[payload_index]
            conjugated = False
            if block_complexity(payload_block) < ALPHA_THRESHOLD:
                payload_block = payload_block ^ board
                conjugated = True

            bit_plane[y : y + BLOCK_SIZE, x : x + BLOCK_SIZE] = payload_block
            positions.append(
                {
                    "y": int(y),
                    "x": int(x),
                    "valid_bits": int(valid_bits),
                    "conjugated": conjugated,
                }
            )
            payload_index += 1

        if payload_index >= len(payload_blocks):
            break

    if payload_index < len(payload_blocks):
        raise RuntimeError(
            f"Not enough complex blocks. Embedded {payload_index}/{len(payload_blocks)} blocks. "
            f"Try lowering ALPHA_THRESHOLD or choosing another frame."
        )

    mask = np.uint8(1 << BIT_PLANE)
    channel = (channel & ~mask) | (bit_plane.astype(np.uint8) << BIT_PLANE)
    frame[:, :, CHANNEL] = channel
    cv2.imwrite(str(frame_path), frame)

    position_data = {
        "method": "BPCS simplified block replacement",
        "frame_index": TARGET_FRAME_INDEX,
        "block_size": BLOCK_SIZE,
        "bit_plane": BIT_PLANE,
        "channel": CHANNEL,
        "alpha_threshold": ALPHA_THRESHOLD,
        "secret_bit_count": len(secret_bits),
        "positions": positions,
    }
    Path(POSITION_FILE).write_text(json.dumps(position_data, indent=2), encoding="utf-8")
    print(f"POSITION_FILE_WRITTEN {POSITION_FILE}")
    print(f"Embedded message length: {len(SECRET_DATA.encode('utf-8'))} bytes")
    print(f"Used blocks: {len(positions)}")

    rebuild_video()
    print(f"Stego video written to {OUTPUT_VIDEO}")


if __name__ == "__main__":
    main()
