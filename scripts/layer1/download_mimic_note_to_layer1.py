from __future__ import annotations

import argparse
import getpass
import hashlib
import re
import shutil
import time
from pathlib import Path


PROJECT_SLUG = "mimic-iv-note"
PROJECT_VERSION = "2.2"
PROJECT_ROOT_NAME = f"{PROJECT_SLUG}-{PROJECT_VERSION}"
BASE_URL = f"https://physionet.org/files/{PROJECT_SLUG}/{PROJECT_VERSION}"
FILES_TO_DOWNLOAD = [
    "LICENSE.txt",
    "SHA256SUMS.txt",
    "note/discharge.csv.gz",
    "note/discharge_detail.csv.gz",
    "note/radiology.csv.gz",
    "note/radiology_detail.csv.gz",
]
MAX_DOWNLOAD_ATTEMPTS = 8
CONNECT_TIMEOUT_SECONDS = 30
READ_TIMEOUT_SECONDS = 600
RETRY_SLEEP_SECONDS = 10
PARALLEL_THRESHOLD_BYTES = 100 * 1024 * 1024
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
RANGE_RESUME_BLOCK_BYTES = 8 * 1024 * 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download the official PhysioNet MIMIC-IV-Note source file set into "
            "Layer 1 raw_original and raw_unpacked."
        )
    )
    parser.add_argument(
        "--layer1-root",
        required=True,
        help="Path to Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-3.1.",
    )
    parser.add_argument(
        "--username",
        required=True,
        help="PhysioNet username or email with approved access to MIMIC-IV-Note.",
    )
    parser.add_argument(
        "--password",
        help="PhysioNet password. If omitted, the script will prompt for it.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Redownload and replace the local note source tree if it already exists.",
    )
    return parser.parse_args()


def require_requests():
    try:
        import requests  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "requests is required. Install it first, for example: `pip install requests`."
        ) from exc
    return requests


def safe_rmtree(path: Path, parent: Path) -> None:
    path = path.resolve()
    parent = parent.resolve()
    if parent not in path.parents:
        raise SystemExit(f"Refusing to remove path outside parent: {path}")
    if path.exists():
        shutil.rmtree(path)


def build_session(requests_module, username: str, password: str):
    session = requests_module.Session()
    login_page = session.get("https://physionet.org/login/", timeout=30)
    login_page.raise_for_status()
    csrf_match = re.search(
        r'<form action="/login/".*?name="csrfmiddlewaretoken" value="([^"]+)"',
        login_page.text,
        flags=re.S,
    )
    if not csrf_match:
        raise SystemExit("Failed to locate PhysioNet login csrf token.")

    response = session.post(
        "https://physionet.org/login/",
        data={
            "csrfmiddlewaretoken": csrf_match.group(1),
            "username": username,
            "password": password,
            "next": "",
            "remember": "on",
        },
        headers={"Referer": "https://physionet.org/login/"},
        timeout=30,
        allow_redirects=True,
    )
    response.raise_for_status()
    logged_in = ("/logout/" in response.text) or ("Sign Out" in response.text) or ("Logout" in response.text)
    if not logged_in:
        raise SystemExit("PhysioNet login failed. Check username/password and access approval.")
    return session


def remote_file_info(session, url: str) -> tuple[int, bool]:
    with session.get(
        url,
        headers={"Range": "bytes=0-0"},
        stream=True,
        timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
    ) as response:
        response.raise_for_status()
        if response.status_code == 206:
            content_range = response.headers.get("Content-Range", "")
            match = re.match(r"bytes \d+-\d+/(\d+)", content_range)
            if not match:
                raise SystemExit(f"Failed to parse Content-Range for {url}: {content_range}")
            return int(match.group(1)), True
        content_length = response.headers.get("Content-Length")
        if not content_length:
            raise SystemExit(f"Failed to determine remote file size for {url}")
        return int(content_length), False


def download_range_part(requests_module, cookies, url: str, part_path: Path, start: int, end: int) -> None:
    headers = {"Range": f"bytes={start}-{end}"}
    for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
        if part_path.exists():
            part_path.unlink()
        try:
            with requests_module.get(
                url,
                headers=headers,
                cookies=cookies,
                stream=True,
                timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
            ) as response:
                response.raise_for_status()
                if response.status_code != 206:
                    raise SystemExit(
                        f"Range request failed for {url}: expected 206, got {response.status_code}"
                    )
                with part_path.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                        if chunk:
                            handle.write(chunk)
            expected_size = end - start + 1
            actual_size = part_path.stat().st_size
            if actual_size != expected_size:
                raise SystemExit(
                    f"Downloaded range size mismatch for {part_path.name}: "
                    f"expected {expected_size}, got {actual_size}"
                )
            return
        except Exception:
            if attempt == MAX_DOWNLOAD_ATTEMPTS:
                raise
            print(
                f"[retry] range download interrupted for {part_path.name}; "
                f"attempt {attempt}/{MAX_DOWNLOAD_ATTEMPTS}"
            )
            time.sleep(RETRY_SLEEP_SECONDS)


def append_part_files(temp_path: Path, part_paths: list[Path]) -> None:
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    with temp_path.open("ab") as destination:
        for part_path in part_paths:
            with part_path.open("rb") as source:
                shutil.copyfileobj(source, destination, length=8 * 1024 * 1024)
            part_path.unlink()


def range_resume_download(requests_module, session, url: str, temp_path: Path, total_size: int) -> None:
    cookies = session.cookies.get_dict()
    current_size = temp_path.stat().st_size if temp_path.exists() else 0
    if current_size > total_size:
        temp_path.unlink()
        current_size = 0
    if current_size == total_size:
        return

    while current_size < total_size:
        start = current_size
        end = min(start + RANGE_RESUME_BLOCK_BYTES - 1, total_size - 1)
        part_path = temp_path.with_name(f"{temp_path.name}.range")
        if part_path.exists():
            part_path.unlink()
        print(f"[range] {temp_path.name} bytes={start}-{end} -> {part_path.name}")
        download_range_part(requests_module, cookies, url, part_path, start, end)
        append_part_files(temp_path, [part_path])
        current_size = temp_path.stat().st_size
        print(f"[resume] {temp_path.name}: {current_size}/{total_size} bytes")


def stream_download(session, url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = destination.with_name(f"tmp_{destination.name}")

    total_size, range_supported = remote_file_info(session, url)
    current_size = temp_path.stat().st_size if temp_path.exists() else 0
    if range_supported and total_size >= PARALLEL_THRESHOLD_BYTES and current_size < total_size:
        range_resume_download(require_requests(), session, url, temp_path, total_size)
    elif current_size == total_size and current_size > 0:
        print(f"[resume] already complete temp file present for {destination.name}")
    else:
        for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
            resume_from = temp_path.stat().st_size if temp_path.exists() else 0
            headers = {}
            mode = "wb"
            if resume_from > 0:
                headers["Range"] = f"bytes={resume_from}-"
                mode = "ab"

            try:
                with session.get(
                    url,
                    stream=True,
                    timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
                    headers=headers,
                ) as response:
                    if resume_from > 0 and response.status_code == 200:
                        # Server ignored Range; restart cleanly rather than appending duplicate bytes.
                        temp_path.unlink()
                        resume_from = 0
                        mode = "wb"
                        response.close()
                        with session.get(
                            url,
                            stream=True,
                            timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
                        ) as restart_response:
                            restart_response.raise_for_status()
                            with temp_path.open(mode) as handle:
                                for chunk in restart_response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                                    if chunk:
                                        handle.write(chunk)
                    else:
                        response.raise_for_status()
                        with temp_path.open(mode) as handle:
                            for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                                if chunk:
                                    handle.write(chunk)
                break
            except Exception:
                if attempt == MAX_DOWNLOAD_ATTEMPTS:
                    raise
                print(
                    f"[retry] download interrupted for {destination.name}; "
                    f"attempt {attempt}/{MAX_DOWNLOAD_ATTEMPTS}, resuming from "
                    f"{temp_path.stat().st_size if temp_path.exists() else 0} bytes"
                )
                time.sleep(RETRY_SLEEP_SECONDS)
                continue
        else:  # pragma: no cover
            raise SystemExit(f"Download failed for {url}")

    if destination.exists():
        destination.unlink()
    temp_path.replace(destination)


def parse_sha256sums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        digest, relative_path = line.split(maxsplit=1)
        checksums[relative_path.strip()] = digest.strip()
    return checksums


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def verify_downloads(raw_original_root: Path) -> None:
    checksum_path = raw_original_root / "SHA256SUMS.txt"
    checksums = parse_sha256sums(checksum_path)
    for relative_path in FILES_TO_DOWNLOAD:
        if relative_path == "SHA256SUMS.txt":
            continue
        expected = checksums.get(relative_path)
        if expected is None:
            raise SystemExit(f"Missing checksum entry for {relative_path} in SHA256SUMS.txt")
        actual = sha256_file(raw_original_root / relative_path)
        if actual != expected:
            raise SystemExit(
                f"Checksum mismatch for {relative_path}: expected {expected}, got {actual}"
            )


def main() -> int:
    args = parse_args()
    password = args.password or getpass.getpass("PhysioNet password: ")
    requests_module = require_requests()

    layer1_root = Path(args.layer1_root).resolve()
    raw_original_root = layer1_root / "raw_original" / PROJECT_ROOT_NAME
    raw_unpacked_root = layer1_root / "raw_unpacked" / "note" / PROJECT_ROOT_NAME

    if raw_original_root.exists():
        if args.overwrite:
            safe_rmtree(raw_original_root, layer1_root / "raw_original")
        else:
            print(f"[resume] reusing existing raw_original note root: {raw_original_root}")
    if raw_unpacked_root.exists():
        if args.overwrite:
            safe_rmtree(raw_unpacked_root, layer1_root / "raw_unpacked" / "note")
        else:
            print(f"[refresh] replacing existing raw_unpacked note root after download: {raw_unpacked_root}")

    session = build_session(requests_module, args.username, password)

    for relative_path in FILES_TO_DOWNLOAD:
        url = f"{BASE_URL}/{relative_path}"
        destination = raw_original_root / relative_path
        print(f"[download] {url} -> {destination}")
        stream_download(session, url, destination)

    verify_downloads(raw_original_root)
    print(f"[verify] SHA256 checks passed under {raw_original_root}")

    if raw_unpacked_root.exists():
        safe_rmtree(raw_unpacked_root, layer1_root / "raw_unpacked" / "note")
    shutil.copytree(raw_original_root, raw_unpacked_root)
    print(f"[copy] {raw_original_root} -> {raw_unpacked_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
