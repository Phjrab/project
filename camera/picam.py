import subprocess
import time
from pathlib import Path


VIDEO_DIR = Path(__file__).resolve().parent / "videos"


def main():
    name = input("저장할 파일명을 입력하세요 (예: myvideo.h264) > ").strip()
    if not name or name in (".", "..") or "/" in name or "\\" in name:
        print("폴더 경로 없이 파일명만 입력하세요.")
        return 1
    if not name.lower().endswith(".h264"):
        name += ".h264"

    output = VIDEO_DIR / name
    try:
        VIDEO_DIR.mkdir(parents=True, exist_ok=True)
        video = output.open("xb")
    except FileExistsError:
        print(f"이미 있는 파일입니다. 다른 이름으로 실행하세요. {output.name}")
        return 1
    except OSError as error:
        print(f"저장 파일을 열 수 없습니다. {error}")
        return 1

    command = [
        "sudo", "rpicam-vid",
        "--timeout", "5000",
        "--width", "640",
        "--height", "480",
        "--framerate", "30",
        "--codec", "h264",
        "--nopreview",
        "--output", "-",
    ]

    print("녹화를 시작합니다.", flush=True)
    start = time.monotonic()
    try:
        with video:
            subprocess.run(command, check=True, stdout=video)
        if output.stat().st_size == 0:
            raise OSError("카메라가 영상 데이터를 반환하지 않았습니다.")
    except KeyboardInterrupt:
        output.unlink(missing_ok=True)
        print("\n녹화를 중단했습니다.")
        return 130
    except (subprocess.CalledProcessError, OSError) as error:
        output.unlink(missing_ok=True)
        print(f"녹화 실패 ({error})")
        return 1

    print(f"녹화 완료 ({time.monotonic() - start:.2f}초)")
    print(f"저장 위치 {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
