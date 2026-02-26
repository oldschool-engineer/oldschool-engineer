"""Download Medium CDN images locally and update post markdown references.

Idempotent: tracks downloaded images in a manifest.json per post directory.
Safe to re-run — skips already-downloaded images, only fetches what's missing.
"""

import json
import re
import time
import urllib.request
from pathlib import Path

POSTS_DIR = Path(r"c:\Users\tom\Documents\GitHub\oldschool-engineer\_posts")
ASSETS_DIR = Path(r"c:\Users\tom\Documents\GitHub\oldschool-engineer\assets\images\posts")
REPO_ROOT = Path(r"c:\Users\tom\Documents\GitHub\oldschool-engineer")

# Regex to match Medium CDN image URLs in markdown
MEDIUM_IMG_RE = re.compile(
    r'https://cdn-images-1\.medium\.com/max/\d+/([^\s\)]+)'
)

# Delay between downloads to avoid 429 rate limiting
DOWNLOAD_DELAY = 2  # seconds


def get_post_slug(filename):
    """Extract slug from post filename (without date prefix and .md)."""
    return re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename.replace('.md', ''))


def guess_extension(url, content_type=None):
    """Guess file extension from URL or content-type header."""
    for ext in ['.png', '.jpeg', '.jpg', '.gif', '.webp', '.svg']:
        if url.lower().endswith(ext):
            return ext
    if content_type:
        ct = content_type.lower()
        if 'png' in ct:
            return '.png'
        if 'jpeg' in ct or 'jpg' in ct:
            return '.jpeg'
        if 'gif' in ct:
            return '.gif'
        if 'webp' in ct:
            return '.webp'
    return '.png'


def load_manifest(img_dir):
    """Load the image manifest (img_id -> local filename) from disk."""
    manifest_path = img_dir / "manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding='utf-8'))
    return {}


def save_manifest(img_dir, manifest):
    """Save the image manifest to disk."""
    manifest_path = img_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')


def download_image(url, dest_path, max_retries=3):
    """Download a single image with retry logic for rate limiting."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                content_type = resp.headers.get('Content-Type', '')
                data = resp.read()

                if not dest_path.suffix:
                    ext = guess_extension(url, content_type)
                    dest_path = dest_path.with_suffix(ext)

                dest_path.parent.mkdir(parents=True, exist_ok=True)
                dest_path.write_bytes(data)
                print(f"  OK  {dest_path.name} ({len(data):,} bytes)")
                return True, dest_path
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                wait = (attempt + 1) * 10  # 10s, 20s, 30s
                print(f"  429 rate limited, waiting {wait}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait)
            else:
                print(f"  FAIL {url}: {e}")
                return False, dest_path
        except Exception as e:
            print(f"  FAIL {url}: {e}")
            return False, dest_path
    return False, dest_path


def process_post(filepath):
    """Process a single post: download missing images, update references."""
    content = filepath.read_text(encoding='utf-8')
    urls = MEDIUM_IMG_RE.findall(content)

    if not urls:
        return 0, 0, 0

    slug = get_post_slug(filepath.name)
    img_dir = ASSETS_DIR / slug
    img_dir.mkdir(parents=True, exist_ok=True)

    # Load manifest of previously downloaded images
    manifest = load_manifest(img_dir)

    # Get unique URLs preserving order
    seen = set()
    unique_urls = []
    for img_id in urls:
        if img_id not in seen:
            seen.add(img_id)
            unique_urls.append(img_id)

    # Determine which images still need downloading
    to_download = [img_id for img_id in unique_urls if img_id not in manifest]
    already_done = len(unique_urls) - len(to_download)

    if to_download:
        print(f"\n{filepath.name} ({len(to_download)} to download, {already_done} cached)")
    elif already_done:
        print(f"\n{filepath.name} (all {already_done} images cached)")

    # Next image number = max existing number + 1 (scan filesystem, not just
    # manifest, so we never collide with files from a prior incomplete run)
    existing_nums = []
    for f in img_dir.glob("img-*"):
        m = re.match(r'img-(\d+)', f.name)
        if m:
            existing_nums.append(int(m.group(1)))
    counter = max(existing_nums, default=0) + 1

    downloaded = 0
    failed = 0

    for img_id in to_download:
        full_url = f"https://cdn-images-1.medium.com/max/1200/{img_id}"

        ext = guess_extension(img_id)
        local_name = f"img-{counter:02d}{ext}"
        dest_path = img_dir / local_name

        # Rate-limit delay between downloads
        if downloaded > 0:
            time.sleep(DOWNLOAD_DELAY)

        success, actual_path = download_image(full_url, dest_path)
        if success:
            manifest[img_id] = actual_path.name
            counter += 1
            downloaded += 1
        else:
            failed += 1

    # Save manifest after any new downloads
    if downloaded > 0:
        save_manifest(img_dir, manifest)

    # Replace all Medium CDN URLs that have a local copy (from this or prior runs)
    def replace_url(match):
        img_id = match.group(1)
        if img_id in manifest:
            local_file = manifest[img_id]
            return f"/assets/images/posts/{slug}/{local_file}"
        return match.group(0)

    new_content = MEDIUM_IMG_RE.sub(replace_url, content)

    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"  Updated {filepath.name}")

    return downloaded, failed, already_done


def main():
    print("Downloading Medium CDN images and updating posts...")
    print(f"Posts dir: {POSTS_DIR}")
    print(f"Assets dir: {ASSETS_DIR}")
    print(f"Delay between downloads: {DOWNLOAD_DELAY}s")
    print()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    total_ok = 0
    total_fail = 0
    total_cached = 0
    for filepath in sorted(POSTS_DIR.glob("*.md")):
        ok, fail, cached = process_post(filepath)
        total_ok += ok
        total_fail += fail
        total_cached += cached

    print(f"\nDone. {total_ok} downloaded, {total_cached} cached, {total_fail} failed.")
    if total_fail > 0:
        print("Re-run the script to retry failed downloads.")


if __name__ == "__main__":
    main()
