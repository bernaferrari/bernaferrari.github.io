#!/usr/bin/env python3
"""Import an already built Compose Web distribution into this Pages site."""

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

SITE = Path(__file__).resolve().parent.parent
DEMOS = {
    "wordkeep": ("markor.js", True),
    "quietguard": ("netguard.js", True),
    "calcula": ("calculator.js", False),
    "sdkmonitor": ("sdkmonitor-demo.js", True),
    "wifi-weakspot": ("wifiweakspot-demo.js", False),
    "keepout": ("shared.js", False),
}


def metadata(source, slug):
    app = next(app for app in json.loads((SITE / "showcase/apps.json").read_text())
               if app["slug"] == slug)
    title = f'{app["name"]} | Browser demo'
    description = app["description"]
    canonical = f"https://bernaferrari.github.io/{slug}/"
    image = f"https://bernaferrari.github.io/showcase/{slug}/social.jpg"
    icon = f"../showcase/{slug}"
    fields = {
        "description": description,
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": description,
        "twitter:image": image,
        "twitter:image:alt": app["alt"],
    }
    if '<meta name="theme-color"' not in source:
        fields["theme-color"] = app["accent"]
    open_graph = {
        "type": "website",
        "site_name": "Bernardo Ferrari’s app demos",
        "title": title,
        "description": description,
        "url": canonical,
        "image": image,
        "image:type": "image/jpeg",
        "image:width": "1200",
        "image:height": "630",
        "image:alt": app["alt"],
    }
    tags = [f"<title>{html.escape(title)}</title>",
            f'<link rel="canonical" href="{canonical}">',
            f'<link rel="icon" href="{icon}/favicon.png" type="image/png" sizes="32x32">',
            f'<link rel="apple-touch-icon" href="{icon}/apple-touch-icon.png" sizes="180x180">']
    tags += [f'<meta name="{key}" content="{html.escape(value)}">' for key, value in fields.items()]
    tags += [f'<meta property="og:{key}" content="{html.escape(value)}">'
             for key, value in open_graph.items()]
    stale_metadata = (
        r"<title>[^<]*</title>"
        r'|<base\s[^>]*>'
        r'|<meta\s+(?:name="(?:description|twitter:[^"]+)"|property="og:[^"]+")[^>]*>'
        r'|<link\s+rel="(?:canonical|icon|apple-touch-icon)"[^>]*>'
        r'|<script type="application/ld\+json">.*?</script>'
    )
    source = re.sub(r"(?m)^[ \t]*(?:" + stale_metadata + r")[ \t]*\n?", "", source, flags=re.S)
    source = source.replace("</head>", "    " + "\n    ".join(tags) + "\n</head>", 1)
    return source.replace("<body>", '<body>\n<noscript>Enable JavaScript to run this demo.</noscript>', 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", choices=DEMOS)
    parser.add_argument("distribution", type=Path)
    parser.add_argument("--license", type=Path)
    parser.add_argument("--source-commit", help="Full Git SHA used to build the distribution")
    args = parser.parse_args()
    if args.source_commit and not re.fullmatch(r"[0-9a-f]{40}", args.source_commit):
        parser.error("--source-commit must be a full Git SHA.")
    entry, sqlite = DEMOS[args.demo]
    distribution = args.distribution.resolve()
    destination = SITE / args.demo
    if distribution == SITE or distribution.is_relative_to(SITE) or SITE.is_relative_to(distribution):
        parser.error("The build distribution must be outside the Pages repository.")
    index = distribution / "index.html"
    if not index.is_file() or not (distribution / entry).is_file():
        parser.error(f"Expected index.html and {entry} in {distribution}")

    page = metadata(index.read_text(encoding="utf-8"), args.demo)
    if sqlite:
        script = f'<script src="{entry}"></script>'
        if script not in page or 'id="loading"' not in page:
            parser.error("Could not find the expected app entry and loading status in index.html.")
        page = page.replace(script, f'<script src="../showcase/isolate.js" data-app="{entry}"></script>')

    license_path = args.license
    existing_license = destination / "LICENSE.txt"
    if license_path is None and existing_license.is_file():
        license_path = existing_license
    if license_path is not None and not license_path.is_file():
        parser.error(f"License file not found: {license_path}")

    with TemporaryDirectory(dir=SITE) as temp:
        staging = Path(temp) / "demo"
        shutil.copytree(distribution, staging, ignore=shutil.ignore_patterns(
            "*.map", "vercel.json", ".DS_Store", ".nojekyll"
        ))
        for name in ("favicon.png", "favicon.ico", "favicon.svg", "opengraph-image.png",
                     "opengraph-image.svg", "social.png"):
            (staging / name).unlink(missing_ok=True)
        # Leave the deployed bundles free of references to omitted source maps.
        for javascript in staging.rglob("*.js"):
            with javascript.open("rb+") as file:
                file.seek(max(0, javascript.stat().st_size - 512))
                tail = file.read()
                marker = re.search(rb"\n//# sourceMappingURL=[^\n]+\s*\Z", tail)
                if marker:
                    file.truncate(file.tell() - len(tail) + marker.start())
        for pattern in ("*.js.LICENSE.txt", "*-OFL.txt"):
            for notice in staging.rglob(pattern):
                lines = notice.read_text(encoding="utf-8").splitlines()
                notice.write_text("\n".join(line.rstrip() for line in lines).rstrip() + "\n",
                                  encoding="utf-8")
        (staging / "index.html").write_text(page, encoding="utf-8")
        if sqlite:
            shutil.copy2(SITE / "showcase/isolation-worker.js", staging)
        if license_path:
            (staging / "LICENSE.txt").write_bytes(license_path.read_bytes().rstrip() + b"\n")
        if args.source_commit:
            (staging / "source-commit.txt").write_text(args.source_commit + "\n", encoding="ascii")

        previous = Path(temp) / "previous"
        if destination.exists():
            destination.rename(previous)
        try:
            staging.rename(destination)
        except OSError:
            if previous.exists():
                previous.rename(destination)
            raise


if __name__ == "__main__":
    main()
