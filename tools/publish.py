#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
              
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
DRAFTS_DIR = REPO_ROOT / "_drafts"
POSTS_DIR = REPO_ROOT / "_posts"
TIMESTAMPS_DIR = REPO_ROOT / "_timestamps"
ARCHIVE_DIR = REPO_ROOT / "_archive"


EXIT_VALID = 0
EXIT_MISSING = 1
EXIT_INVALID = 2
EXIT_USAGE = 3


def die(msg: str, code: int = 1) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def run(
    cmd: list[str],
    *,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
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


def lineage_name_from_draft(draft_path: Path) -> str:
    return strip_date_prefix(draft_path.name)


def current_proof_path_for_draft(draft_path: Path) -> Path:
    return TIMESTAMPS_DIR / f"{lineage_name_from_draft(draft_path)}.proof.json"


def current_post_path_for_draft(draft_path: Path) -> Path:
    return POSTS_DIR / lineage_name_from_draft(draft_path)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        die(f"JSON file must contain an object: {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ---------------------------------------------------------------------
# INDEX LEDGER
# ---------------------------------------------------------------------
                     
# Yes, I've assumed a hash algorithm... will fix later
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def current_revision_for_draft(draft_path: Path) -> int:
    proof_path = current_proof_path_for_draft(draft_path)
    if not proof_path.exists():
        return 0

    doc = load_json(proof_path)
    revision = doc.get("revision", 1)
    if not isinstance(revision, int) or revision < 1:
        die(f"Invalid revision in proof bundle: {proof_path}")
    return revision


def next_revision_for_draft(draft_path: Path) -> int:
    current = current_revision_for_draft(draft_path)
    return 1 if current == 0 else current + 1


def set_proof_revision(proof_path: Path, revision: int) -> None:
    doc = load_json(proof_path)
    doc["revision"] = revision
    write_json(proof_path, doc)


def update_index() -> Path:
    index_path = TIMESTAMPS_DIR / "index.json"
                

    entries: list[dict[str, Any]] = []
    for proof in sorted(TIMESTAMPS_DIR.glob("*.proof.json")):
        post_name = proof.name.removesuffix(".proof.json")
                       
        entry: dict[str, Any] = {
            "post": f"_posts/{post_name}",
            "proof": f"_timestamps/{proof.name}",
            "proof_sha256": sha256_file(proof),
        }

        try:
            proof_doc = load_json(proof)
            revision = proof_doc.get("revision")
            if isinstance(revision, int) and revision >= 1:
                entry["revision"] = revision
        except Exception:
            pass

        entries.append(entry)

    index = {
        "schema": "north-shadow.index",
        "version": 1,
        "posts": entries,
    }

    write_json(index_path, index)
                                     
                     

    print(f"Updated index: {index_path}")
    return index_path


# ---------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------

def decode_embedded_content(proof_path: Path) -> bytes:
    doc = load_json(proof_path)

    try:
        value = doc["content"]["value"]
    except Exception:
        die(f"Malformed proof bundle, missing content.value: {proof_path}")

    if not isinstance(value, str):
        die(f"Malformed proof bundle, content.value must be a base64 string: {proof_path}")

    try:
        return base64.b64decode(value, validate=True)
    except Exception:
        die(f"Malformed proof bundle, invalid base64 in content.value: {proof_path}")


def validate_proof_only(proof_path: Path) -> int:
    proc = run([str(TOOLS_DIR / "validate.sh"), str(proof_path)], check=False)
    return proc.returncode


def validate_draft_against_proof(draft_path: Path, proof_path: Path) -> int:
    proc = run(
        [str(TOOLS_DIR / "validate.sh"), str(proof_path), str(draft_path)],
        check=False,
    )
    return proc.returncode


# ---------------------------------------------------------------------
# STAMPING
# ---------------------------------------------------------------------

def stamp_post(path: Path) -> None:
    run([str(TOOLS_DIR / "stamp.sh"), str(path)])


                                                
                        

                         
                                                       
                                                       
                          
                          


# ---------------------------------------------------------------------
# GIT
# ---------------------------------------------------------------------																	   

def git_has_staged_changes() -> bool:
    proc = run(["git", "diff", "--cached", "--quiet"], check=False)
    return proc.returncode != 0


def add_for_commit(paths: list[Path]) -> None:
    if not paths:
        return
    run(["git", "add", "--", *[str(p) for p in paths]])


def git_commit(message: str) -> None:
    run(["git", "commit", "-m", message])


def git_push() -> None:
    run(["git", "push"])


def stage_commit_and_maybe_push(paths: list[Path], message: str, *, push: bool = True) -> None:
    add_for_commit(paths)

    if not git_has_staged_changes():
        print("No changes to commit.")
        return

    git_commit(message)

    if push:
        git_push()
    else:
        print("Committed locally. Skipping push (--no-push).")


# ---------------------------------------------------------------------
# CORE PUBLISH
# ---------------------------------------------------------------------

def archive_slug_dirname(draft_path: Path) -> str:
    return lineage_name_from_draft(draft_path).removesuffix(".md")


def archive_revision_dir(draft_path: Path) -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    return ARCHIVE_DIR / archive_slug_dirname(draft_path) / stamp


def archive_current_truth(draft_path: Path) -> tuple[Path, list[Path]]:
    proof_path = current_proof_path_for_draft(draft_path)
    post_path = current_post_path_for_draft(draft_path)

    dest_dir = archive_revision_dir(draft_path)
    dest_dir.mkdir(parents=True, exist_ok=False)

    archived_paths: list[Path] = []

    for suffix in (".p7s", ".p7s.tsq", ".p7s.tsr"):
        sidecar = TIMESTAMPS_DIR / f"{lineage_name_from_draft(draft_path)}{suffix}"
        if sidecar.exists():
            dest = dest_dir / sidecar.name
            shutil.copy2(sidecar, dest)
            archived_paths.append(dest)

    if proof_path.exists():
        dest = dest_dir / proof_path.name
        shutil.copy2(proof_path, dest)
        archived_paths.append(dest)

    if post_path.exists():
        dest = dest_dir / post_path.name
        shutil.copy2(post_path, dest)
        archived_paths.append(dest)

    if not archived_paths:
        shutil.rmtree(dest_dir)
        die(f"Nothing current to archive for {lineage_name_from_draft(draft_path)}")

    return dest_dir, archived_paths


def materialize_post_from_draft(draft_path: Path) -> Path:
    post_path = current_post_path_for_draft(draft_path)
    post_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(draft_path, post_path)
    return post_path


def rename_generated_proof(post_path: Path, draft_path: Path) -> Path:
    generated = TIMESTAMPS_DIR / f"{post_path.name}.proof.json"
    target = current_proof_path_for_draft(draft_path)

    if not generated.exists():
        die(f"stamp.sh did not produce proof bundle: {generated}")

    target.parent.mkdir(parents=True, exist_ok=True)
    if generated.resolve() != target.resolve():
        if target.exists():
            target.unlink()
        generated.replace(target)

    return target


def cleanup_legacy_sidecars(post_path: Path) -> None:
    KEEP_SIDECARS = True
    if not KEEP_SIDECARS:
        for suffix in (".p7s", ".p7s.tsq", ".p7s.tsr"):
            p = TIMESTAMPS_DIR / f"{post_path.name}{suffix}"
            if p.exists():
                p.unlink()


def publish_new_current(draft_path: Path) -> tuple[Path, Path]:
    post_path = materialize_post_from_draft(draft_path)

    stamp_post(post_path)

    proof_path = rename_generated_proof(post_path, draft_path)
    set_proof_revision(proof_path, next_revision_for_draft(draft_path))

    cleanup_legacy_sidecars(post_path)

    status = validate_draft_against_proof(draft_path, proof_path)

    if status != EXIT_VALID:
        die(f"Post-stamp validation failed for {proof_path} with exit code {status}")

    index_path = update_index()

                                       

    return proof_path, index_path


                                                                       
               
                                                                       

def first_publish(draft_path: Path, *, push: bool) -> None:
    proof_path, index_path = publish_new_current(draft_path)

    stage_commit_and_maybe_push(
        [
            current_post_path_for_draft(draft_path),
            proof_path,
            index_path,
        ],
        f"publish: {lineage_name_from_draft(draft_path)}",
        push=push,
    )

    print(f"Published: {lineage_name_from_draft(draft_path)}")


def repair_current_projection_or_proof(
    draft_path: Path,
    proof_path: Path,
    assume_yes: bool,
    *,
    push: bool,
) -> None:
    proof_status = validate_proof_only(proof_path)
    post_path = current_post_path_for_draft(draft_path)
    post_matches_truth = post_path.exists() and post_path.read_bytes() == decode_embedded_content(proof_path)

    if proof_status == EXIT_VALID and post_matches_truth:
        print("Draft already matches current attested content. Skipping.")
                                            
        return

                                                                       

    if proof_status == EXIT_VALID and not post_matches_truth:
        print("Current proof is valid, but _posts projection is stale. Refreshing projection.")
        shutil.copy2(draft_path, post_path)
        index_path = update_index()
        stage_commit_and_maybe_push(
            [post_path, index_path],
            f"publish: {lineage_name_from_draft(draft_path)}",
            push=push,
        )
        print(f"Refreshed projection: {post_path.relative_to(REPO_ROOT)}")
        return

    if proof_status == EXIT_INVALID:
        if not assume_yes and not confirm(
            "Draft matches current attested content, but current proof is invalid. Rebuild current proof? [y/N] "
        ):
            die("Aborted by user.")
        print("Rebuilding current proof from draft.")
    elif proof_status == EXIT_MISSING:
        print("Current proof is missing. Rebuilding current proof from draft.")
    else:
        die(f"Validation failed unexpectedly for {proof_path} with exit code {proof_status}")

    new_proof_path, index_path = publish_new_current(draft_path)

    stage_commit_and_maybe_push(
        [
            current_post_path_for_draft(draft_path),
            new_proof_path,
            index_path,
        ],
        f"publish: {lineage_name_from_draft(draft_path)}",
        push=push,
    )
    print(f"Rebuilt current truth for: {lineage_name_from_draft(draft_path)}")


def replace_current_truth(draft_path: Path, assume_yes: bool, *, push: bool) -> None:
    if not assume_yes and not confirm("Draft differs from current attested content. Replace? [y/N] "):
        die("Aborted by user.")

    archive_dir, archived_paths = archive_current_truth(draft_path)
    print(f"Archived current truth to: {archive_dir.relative_to(REPO_ROOT)}")

    proof_path, index_path = publish_new_current(draft_path)

    stage_commit_and_maybe_push(
        [
            current_post_path_for_draft(draft_path),
            proof_path,
            index_path,
            *archived_paths,
        ],
        f"publish: {lineage_name_from_draft(draft_path)}",
        push=push,
    )
    print(f"Published updated version: {lineage_name_from_draft(draft_path)}")


                                                  
                                                                  


                                                   
                                                                           
                                                                 


def publish_draft(draft_path: Path, assume_yes: bool = False, *, push: bool = True) -> None:
    proof_path = current_proof_path_for_draft(draft_path)
                                                       

    if not proof_path.exists():
        print(f"No current proof found. Publishing: {lineage_name_from_draft(draft_path)}")
        first_publish(draft_path, push=push)
        return

    match_status = validate_draft_against_proof(draft_path, proof_path)
                                                                                   
                            
                                                          
                               

    if match_status == EXIT_VALID:
        repair_current_projection_or_proof(
            draft_path,
            proof_path,
            assume_yes=assume_yes,
            push=push,
        )
        return

    if match_status == EXIT_MISSING:
        print("Current proof path resolved but proof is missing. Rebuilding current truth.")
        new_proof_path, index_path = publish_new_current(draft_path)
        stage_commit_and_maybe_push(
            [
                current_post_path_for_draft(draft_path),
                new_proof_path,
                index_path,
            ],
            f"publish: {lineage_name_from_draft(draft_path)}",
            push=push,
        )
        print(f"Published: {lineage_name_from_draft(draft_path)}")
        return

    if match_status == EXIT_INVALID:
        replace_current_truth(draft_path, assume_yes=assume_yes, push=push)
        return

    die(f"Validation failed unexpectedly for {proof_path} with exit code {match_status}")


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Publish a markdown draft from _drafts/ using attestation bundles in _timestamps/ "
            "as the current canonical truth, archive replaced versions, materialize _posts/, and push."
        )
    )
    parser.add_argument("draft", help="Path to a markdown file under _drafts/")
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Auto-confirm replacement when draft differs from current attested content or current proof is invalid.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Create the local commit but do not push to the remote.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    require_repo_paths()

    draft_path = resolve_draft_path(args.draft)
    publish_draft(draft_path, assume_yes=args.yes, push=not args.no_push)
                  
                   
                            
                              
     


if __name__ == "__main__":
    main()