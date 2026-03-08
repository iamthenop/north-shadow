#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
DRAFTS_DIR = REPO_ROOT / "_drafts"
POSTS_DIR = REPO_ROOT / "_posts"
TIMESTAMPS_DIR = REPO_ROOT / "_timestamps"
ARCHIVE_DIR = REPO_ROOT / "_archive"


def die(msg: str, code: int = 1) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def run(cmd: list[str], check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        check=check,
        text=True,
        capture_output=capture,
    )


def confirm(prompt: str) -> bool:
    try:
        reply = input(prompt).strip().lower()
    except EOFError:
        return False
    return reply in {"y", "yes"}


def is_markdown_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".md"


def require_repo_paths() -> None:
    if not TOOLS_DIR.is_dir():
        die(f"Missing tools directory: {TOOLS_DIR}")
    if not DRAFTS_DIR.is_dir():
        die(f"Missing drafts directory: {DRAFTS_DIR}")
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    TIMESTAMPS_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def resolve_draft_path(user_arg: str) -> Path:
    p = Path(user_arg)
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()

    if not is_markdown_file(p):
        die(f"Draft not found or not markdown: {p}")

    try:
        p.relative_to(DRAFTS_DIR.resolve())
    except ValueError:
        die(f"Draft must be under {DRAFTS_DIR}")

    return p


def strip_date_prefix(name: str) -> str:
    if len(name) > 14 and name[:10].count("-") == 2 and name[10] == "-":
        maybe_date = name[:10]
        try:
            dt.date.fromisoformat(maybe_date)
            return name[11:]
        except ValueError:
            return name
    return name


def post_tail_from_draft(draft_path: Path) -> str:
    return strip_date_prefix(draft_path.name)


def draft_to_post_basename(draft_path: Path, today: dt.date) -> str:
    return f"{today.isoformat()}-{post_tail_from_draft(draft_path)}"


def find_existing_post_for_draft(draft_path: Path) -> Path | None:
    tail = post_tail_from_draft(draft_path)
    matches = sorted(POSTS_DIR.glob(f"*-{tail}"))
    if not matches:
        return None
    if len(matches) > 1:
        die(f"Multiple published posts match draft basename '{tail}': {[m.name for m in matches]}")
    return matches[0]


def files_equal(a: Path, b: Path) -> bool:
    return a.read_bytes() == b.read_bytes()


def validate_post(post_path: Path) -> int:
    proc = run([str(TOOLS_DIR / "validate.sh"), str(post_path)], check=False)
    return proc.returncode


def stamp_post(post_path: Path) -> None:
    run([str(TOOLS_DIR / "stamp.sh"), str(post_path)])


def git_has_staged_changes() -> bool:
    proc = run(["git", "diff", "--cached", "--quiet"], check=False)
    return proc.returncode != 0


def git_commit_and_push(message: str) -> None:
    run(["git", "commit", "-m", message])
    run(["git", "push"])


def add_for_commit(paths: list[Path]) -> None:
    run(["git", "add", *[str(p) for p in paths]])


def timestamp_artifact_paths(post_path: Path) -> list[Path]:
    base = post_path.name
    return [
        TIMESTAMPS_DIR / f"{base}.p7s",
        TIMESTAMPS_DIR / f"{base}.p7s.tsq",
        TIMESTAMPS_DIR / f"{base}.p7s.tsr",
    ]


def archive_slug_dirname(post_path: Path) -> str:
    return strip_date_prefix(post_path.name).removesuffix(".md")


def archive_revision_dir(post_path: Path) -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    return ARCHIVE_DIR / archive_slug_dirname(post_path) / stamp


def archive_existing_bundle(post_path: Path) -> Path:
    dest_dir = archive_revision_dir(post_path)
    dest_dir.mkdir(parents=True, exist_ok=False)

    archived_any = False

    if post_path.exists():
        shutil.copy2(post_path, dest_dir / post_path.name)
        archived_any = True

    for artifact in timestamp_artifact_paths(post_path):
        if artifact.exists():
            shutil.copy2(artifact, dest_dir / artifact.name)
            archived_any = True

    if not archived_any:
        shutil.rmtree(dest_dir)
        die(f"Nothing to archive for {post_path}")

    return dest_dir


def replace_published_content(draft_path: Path, post_path: Path) -> None:
    shutil.copy2(draft_path, post_path)


def first_publish(draft_path: Path) -> None:
    today = dt.date.today()
    post_path = POSTS_DIR / draft_to_post_basename(draft_path, today)

    print(f"No published post found. Creating: {post_path.relative_to(REPO_ROOT)}")
    replace_published_content(draft_path, post_path)
    stamp_post(post_path)

    status = validate_post(post_path)
    if status != 0:
        die(f"Post-stamp validation failed for {post_path} with exit code {status}")

    add_for_commit([draft_path, post_path, TIMESTAMPS_DIR])
    if not git_has_staged_changes():
        print("No changes to commit.")
        return

    git_commit_and_push(f"publish: {post_path.name}")
    print(f"Published: {post_path.relative_to(REPO_ROOT)}")


def repair_proof_only(draft_path: Path, post_path: Path, assume_yes: bool) -> None:
    validation_status = validate_post(post_path)

    if validation_status == 0:
        print("Published post already matches draft and has valid proof. Skipping.")
        return

    if validation_status == 1:
        print("Published post matches draft, but proof is missing. Restamping.")
    elif validation_status == 2:
        if not assume_yes and not confirm(
            "Published content matches draft, but proof is invalid. Replace proof bundle? [y/N] "
        ):
            die("Aborted by user.")
        print("Replacing invalid proof bundle.")
    else:
        die(f"Unexpected validation status: {validation_status}")

    stamp_post(post_path)

    status = validate_post(post_path)
    if status != 0:
        die(f"Post-stamp validation failed for {post_path} with exit code {status}")

    add_for_commit([draft_path, post_path, TIMESTAMPS_DIR])
    if not git_has_staged_changes():
        print("No changes to commit.")
        return

    git_commit_and_push(f"publish: {post_path.name}")
    print(f"Repaired proof for: {post_path.relative_to(REPO_ROOT)}")


def replace_with_archive(draft_path: Path, post_path: Path, assume_yes: bool) -> None:
    if not assume_yes and not confirm(
        "Draft differs from published post. Archive current published version and replace it? [y/N] "
    ):
        die("Aborted by user.")

    archive_dir = archive_existing_bundle(post_path)
    print(f"Archived current published bundle to: {archive_dir.relative_to(REPO_ROOT)}")

    replace_published_content(draft_path, post_path)
    stamp_post(post_path)

    status = validate_post(post_path)
    if status != 0:
        die(f"Post-stamp validation failed for {post_path} with exit code {status}")

    add_for_commit([draft_path, post_path, TIMESTAMPS_DIR, archive_dir])
    if not git_has_staged_changes():
        print("No changes to commit.")
        return

    git_commit_and_push(f"publish: {post_path.name}")
    print(f"Published updated version: {post_path.relative_to(REPO_ROOT)}")


def publish_draft(draft_path: Path, assume_yes: bool = False) -> None:
    existing_post = find_existing_post_for_draft(draft_path)

    if existing_post is None:
        first_publish(draft_path)
        return

    post_path = existing_post
    print(f"Found existing published post: {post_path.relative_to(REPO_ROOT)}")

    same_content = files_equal(draft_path, post_path)

    if same_content:
        repair_proof_only(draft_path, post_path, assume_yes=assume_yes)
        return

    replace_with_archive(draft_path, post_path, assume_yes=assume_yes)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish a markdown draft from _drafts/ to _posts/, archive replaced versions, stamp, validate, and push."
    )
    parser.add_argument("draft", help="Path to a markdown file under _drafts/")
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Auto-confirm replacement when draft differs or proof is invalid.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    require_repo_paths()
    draft_path = resolve_draft_path(args.draft)
    publish_draft(draft_path, assume_yes=args.yes)


if __name__ == "__main__":
    main()