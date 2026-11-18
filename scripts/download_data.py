"""Download the raw data into data/raw/ (not committed).

Run from the repository root:
    python scripts/download_data.py            # skip files that already exist
    python scripts/download_data.py --force    # download everything again

1. Big Mac index (The Economist, CC BY 4.0), read through the GitHub REST API: the API answers in JSON
   with the file content (base64) and its version (blob sha), which is saved in big-mac-version.json.
   If the API is unavailable (rate limit: 60 requests/hour), the raw file URL is used instead.
2. Brent daily spot price (EIA series RBRTE), downloaded directly from EIA only.
3. Energy Institute: PDF tables are included under references/ and data/ei_pdf_2026/;
   run scripts/extract_ei_pdf.py to re-extract 2015–2025 values. This is not
   a source for the entire 1965–2025 historical table.
"""

import argparse
import base64
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TIMEOUT = 60  # seconds
HEADERS = {"User-Agent": "ie421-data-pilgrims"}

BIGMAC_REPO = "TheEconomist/big-mac-data"
BIGMAC_FILES = {  # local name -> path in the GitHub repository
    "big-mac-full-index.csv": "output-data/big-mac-full-index.csv",       # main dataset
    "big-mac-source-data-v2.csv": "source-data/big-mac-source-data-v2.csv",  # cross-check only
}
BRENT_URL = "https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls"
EI_INFO = "  PDF-derived oil tables supplied (2015–2025 only); run python scripts/extract_ei_pdf.py."


def get(url: str) -> requests.Response:
    response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    response.raise_for_status()
    return response


def download_bigmac(force: bool) -> bool:
    """Read each Big Mac file through the GitHub contents API (JSON) and record its version."""
    versions, ok = {}, True
    for name, repo_path in BIGMAC_FILES.items():
        target = RAW / name
        if target.exists() and not force:
            print(f"  exists, skipped: {name}")
            continue
        try:
            meta = get(f"https://api.github.com/repos/{BIGMAC_REPO}/contents/{repo_path}").json()
            if meta.get("encoding") != "base64":
                raise ValueError("Unexpected GitHub API content encoding")
            payload = base64.b64decode(meta["content"])
            if not payload.lstrip().startswith(b"date,"):
                raise ValueError("Big Mac response does not appear to be CSV")
            target.write_bytes(payload)
            versions[name] = {"source": f"github.com/{BIGMAC_REPO}/{repo_path}", "sha": meta["sha"],
                              "accessed": datetime.now(timezone.utc).date().isoformat(), "via": "GitHub REST API (JSON)"}
        except Exception as err:  # noqa: BLE001 - API limit or network: fall back to the raw URL
            print(f"  GitHub API failed for {name} ({err}); using the raw file URL")
            try:
                payload = get(f"https://raw.githubusercontent.com/{BIGMAC_REPO}/master/{repo_path}").content
                if not payload.lstrip().startswith(b"date,"):
                    raise ValueError("Raw GitHub response does not appear to be CSV")
                target.write_bytes(payload)
                versions[name] = {"source": f"github.com/{BIGMAC_REPO}/{repo_path}",
                                  "accessed": datetime.now(timezone.utc).date().isoformat(), "via": "raw URL"}
            except Exception as err2:  # noqa: BLE001
                print(f"  FAILED {name}: {err2}")
                ok = False
                continue
        print(f"  saved {name} ({target.stat().st_size / 1024:.0f} KB)")
    if versions:
        version_path = RAW / "big-mac-version.json"
        previous = json.loads(version_path.read_text()) if version_path.exists() else {}
        previous.update(versions)
        version_path.write_text(json.dumps(previous, indent=2), encoding="utf-8")
    return ok


def download_brent(force: bool) -> bool:
    """Download Brent spot prices directly from the EIA; fail explicitly if unavailable."""
    target = RAW / "RBRTEd.xls"
    if target.exists() and not force:
        print("  exists, skipped: RBRTEd.xls")
        return True
    try:
        content = get(BRENT_URL).content
        if len(content) < 1000 or not content.startswith(bytes.fromhex("D0CF11E0")):
            raise ValueError("EIA response is not a valid legacy Excel .xls file")
        target.write_bytes(content)
        print(f"  saved {target.name} ({len(content) / 1024:.0f} KB)")
        return True
    except Exception as err:
        print(f"  EIA Brent download failed ({err})")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="download again even if the file exists")
    force = parser.parse_args().force

    RAW.mkdir(parents=True, exist_ok=True)
    print("1/3 Big Mac index (The Economist, GitHub API)")
    ok = download_bigmac(force)
    print("2/3 Brent daily spot price (EIA only)")
    ok = download_brent(force) and ok
    print("3/3 Energy Institute PDF-derived tables (local source)")
    print(EI_INFO)

    print("Done." if ok else "Some downloads failed; see messages above.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
