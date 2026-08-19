from pathlib import Path
import shutil


DOWNLOADS = Path(r"C:\Users\student\Downloads")

FILE_GROUPS = {
    "images": {".jpg", ".jpeg"},
    "data": {".csv", ".xlsx"},
    "docs": {".txt", ".doc", ".pdf"},
    "archive": {".zip"},
}


def get_unique_path(destination: Path) -> Path:
    """같은 이름의 파일이 있으면 새 이름을 반환합니다."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def organize_downloads() -> None:
    if not DOWNLOADS.exists():
        print(f"다운로드 폴더를 찾을 수 없습니다: {DOWNLOADS}")
        return

    for folder_name in FILE_GROUPS:
        (DOWNLOADS / folder_name).mkdir(exist_ok=True)

    moved_count = 0
    for file_path in DOWNLOADS.iterdir():
        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()
        destination_folder = next(
            (
                DOWNLOADS / folder_name
                for folder_name, extensions in FILE_GROUPS.items()
                if extension in extensions
            ),
            None,
        )
        if destination_folder is None:
            continue

        destination = get_unique_path(destination_folder / file_path.name)
        shutil.move(str(file_path), str(destination))
        print(f"이동: {file_path.name} -> {destination_folder.name}")
        moved_count += 1

    print(f"정리 완료: {moved_count}개 파일")


if __name__ == "__main__":
    organize_downloads()