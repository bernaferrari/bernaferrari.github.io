#!/usr/bin/env python3
"""Rebuild browser demos whose published source commits have changed."""

import argparse
import fcntl
import json
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

SITE = Path(__file__).resolve().parent.parent
APPS_FILE = SITE / "showcase/apps.json"
SOURCE_BRANCH = "main"


def git_output(*args, cwd=SITE):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def update(app, dry_run):
    slug = app["slug"]
    url = f"https://github.com/bernaferrari/{app['repo']}.git"
    current = SITE / slug / "source-commit.txt"
    installed = current.read_text(encoding="ascii").strip() if current.is_file() else ""
    remote = git_output("ls-remote", "--exit-code", url, f"refs/heads/{SOURCE_BRANCH}")
    revision = remote.split()[0]
    if revision == installed and (current.parent / "index.html").is_file():
        print(f"{slug}: up to date ({revision[:12]})", flush=True)
        return

    print(f"{slug}: {installed[:12] or 'untracked'} → {revision[:12]}", flush=True)
    if dry_run:
        return

    with TemporaryDirectory(prefix=f"pages-{slug}-") as temp:
        source = Path(temp) / "source"
        subprocess.run(
            ["git", "clone", "--quiet", "--depth", "1", "--branch", SOURCE_BRANCH, url, source],
            check=True,
        )
        if git_output("rev-parse", "HEAD", cwd=source) != revision:
            raise RuntimeError("The source branch moved during clone. Run the updater again.")
        if (source / ".gitmodules").is_file():
            subprocess.run(["git", "submodule", "update", "--init", "--recursive"],
                           cwd=source, check=True)
        if app.get("platform") == "flutter":
            build_root = source / app.get("buildDirectory", ".")
            subprocess.run(
                ["flutter", "build", "web", "--release", "--base-href", f"/{slug}/",
                 *app.get("buildArgs", [])],
                cwd=build_root, check=True,
            )
            distribution = build_root / "build/web"
        else:
            module = app["module"]
            subprocess.run(
                ["./gradlew", f":{module}:wasmJsBrowserDistribution", "--console=plain"],
                cwd=source, check=True, env={**os.environ, "COREPACK_ENABLE_PROJECT_SPEC": "0"},
            )
            distribution = source / module / "build/dist/wasmJs/productionExecutable"
        command = [
            sys.executable, SITE / "scripts/import-demo.py", slug, distribution,
            "--source-commit", revision,
        ]
        if "socialCard" in app:
            command += ["--social-card", source / app["socialCard"]["source"]]
        if (source / "LICENSE").is_file():
            command += ["--license", source / "LICENSE"]
        subprocess.run(command, check=True)
        print(f"{slug}: imported {revision[:12]}", flush=True)


def main():
    apps = {app["slug"]: app for app in json.loads(APPS_FILE.read_text(encoding="utf-8"))}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demos", nargs="*", metavar="demo", help="Demo paths (default: all managed demos)")
    parser.add_argument("--dry-run", action="store_true", help="Check revisions without building")
    args = parser.parse_args()
    for slug in args.demos:
        if slug not in apps:
            parser.error(f"Unknown demo {slug!r}. Choose from {', '.join(apps)}.")

    # Keep the lock outside the published site and share it across updater runs.
    lock_path = Path(git_output("rev-parse", "--path-format=absolute", "--git-path", "update-demos.lock"))
    failed = False
    with lock_path.open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("Another demo update is running in this checkout.")
        for slug in dict.fromkeys(args.demos or apps):
            try:
                update(apps[slug], args.dry_run)
            except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
                print(f"{slug}: update failed: {error}", file=sys.stderr, flush=True)
                failed = True
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
