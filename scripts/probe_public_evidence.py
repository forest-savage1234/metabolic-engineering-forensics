#!/usr/bin/env python3
"""Probe public publication artifacts without committing third-party source files.

Downloads are ephemeral. The script records URLs, byte sizes, SHA-256 digests,
archive/workbook structure, and locations of bounded target values. It never
commits or republishes the downloaded source artifacts.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from dataclasses import dataclass, asdict
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook

UA = "metabolic-engineering-forensics/0.1 (+research artifact verification)"
TIMEOUT = 60


@dataclass
class Probe:
    case: str
    label: str
    landing_url: str
    resolved_url: str | None = None
    status_code: int | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    sha256: str | None = None
    workbook_sheets: list[dict] | None = None
    archive_members: list[str] | None = None
    target_hits: list[dict] | None = None
    error: str | None = None


def get(url: str) -> requests.Response:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT, allow_redirects=True)
    r.raise_for_status()
    return r


def find_download(landing_url: str, anchor_pattern: str) -> str:
    r = get(landing_url)
    soup = BeautifulSoup(r.text, "html.parser")
    pattern = re.compile(anchor_pattern, re.I)
    candidates: list[tuple[str, str]] = []
    for a in soup.find_all("a", href=True):
        text = " ".join(a.stripped_strings)
        href = a.get("href")
        if pattern.search(text):
            candidates.append((text, urljoin(r.url, href)))
    if not candidates:
        raise RuntimeError(f"no anchor matching {anchor_pattern!r} at {landing_url}")
    # Prefer links whose text explicitly contains download/source/dataset terminology.
    candidates.sort(key=lambda x: ("download" not in x[0].lower(), len(x[0])))
    return candidates[0][1]


def workbook_inventory(data: bytes, targets: Iterable[str]) -> tuple[list[dict], list[dict]]:
    wb = load_workbook(io.BytesIO(data), read_only=True, data_only=False)
    sheets: list[dict] = []
    hits: list[dict] = []
    target_set = {str(t).strip() for t in targets}
    for ws in wb.worksheets:
        sheets.append({"title": ws.title, "max_row": ws.max_row, "max_column": ws.max_column})
        for row in ws.iter_rows():
            for cell in row:
                v = cell.value
                if v is None:
                    continue
                sv = str(v).strip()
                # Exact numeric/string target hits are most defensible; also permit a
                # compact substring hit for units embedded in textual labels.
                if sv in target_set or any(t in sv for t in target_set if len(t) >= 4):
                    hits.append({"sheet": ws.title, "cell": cell.coordinate, "value": sv[:300]})
                    if len(hits) >= 100:
                        return sheets, hits
    return sheets, hits


def probe_download(case: str, label: str, landing: str, download_url: str, targets: list[str]) -> Probe:
    p = Probe(case=case, label=label, landing_url=landing)
    try:
        r = get(download_url)
        data = r.content
        p.resolved_url = r.url
        p.status_code = r.status_code
        p.content_type = r.headers.get("content-type")
        p.size_bytes = len(data)
        p.sha256 = hashlib.sha256(data).hexdigest()
        if zipfile.is_zipfile(io.BytesIO(data)):
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                p.archive_members = zf.namelist()
                # Inspect contained workbooks for target values without retaining bytes.
                all_sheets: list[dict] = []
                all_hits: list[dict] = []
                for name in zf.namelist():
                    if name.lower().endswith(".xlsx"):
                        try:
                            sheets, hits = workbook_inventory(zf.read(name), targets)
                            for item in sheets:
                                item["archive_member"] = name
                            for item in hits:
                                item["archive_member"] = name
                            all_sheets.extend(sheets)
                            all_hits.extend(hits)
                        except Exception as exc:  # retain probe even if one workbook is malformed
                            all_sheets.append({"archive_member": name, "error": str(exc)})
                p.workbook_sheets = all_sheets or None
                p.target_hits = all_hits or None
        elif download_url.lower().endswith(".xlsx") or "spreadsheet" in (p.content_type or "") or data[:2] == b"PK":
            sheets, hits = workbook_inventory(data, targets)
            p.workbook_sheets = sheets
            p.target_hits = hits
    except Exception as exc:
        p.error = f"{type(exc).__name__}: {exc}"
    return p


def main() -> int:
    specs = [
        {
            "case": "kim-2019",
            "label": "Supplementary Dataset 1 — raw fed-batch fermentations",
            "landing": "https://www.nature.com/articles/s41589-019-0295-5",
            "anchor": r"Supplementary Dataset 1",
            "targets": ["50.2", "47.2", "46.7", "49.2", "50.1"],
        },
        {
            "case": "park-2022",
            "label": "Source Data Fig. 7 — final lutein fed-batch",
            "landing": "https://www.nature.com/articles/s41929-022-00820-4",
            "anchor": r"Source Data Fig\. 7",
            "targets": ["218", "218.0", "5.01", "LUT5MH1"],
        },
        {
            "case": "cho-2026",
            "label": "Figshare source-data archive",
            "landing": "https://springernature.figshare.com/articles/dataset/Cho_and_Prabowo-etal-Source_data/29264624",
            "anchor": r"Download",
            "targets": ["141.5", "2.95", "SC97"],
        },
    ]

    results: list[Probe] = []
    for spec in specs:
        try:
            url = find_download(spec["landing"], spec["anchor"])
            result = probe_download(spec["case"], spec["label"], spec["landing"], url, spec["targets"])
        except Exception as exc:
            result = Probe(
                case=spec["case"], label=spec["label"], landing_url=spec["landing"],
                error=f"{type(exc).__name__}: {exc}",
            )
        results.append(result)

    payload = {
        "schema_version": 1,
        "principle": "Downloaded third-party bytes are ephemeral; only provenance metadata and bounded-value locations are emitted.",
        "probes": [asdict(p) for p in results],
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
    print(text)
    with open("probe-results.json", "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    return 0 if all(p.error is None for p in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
