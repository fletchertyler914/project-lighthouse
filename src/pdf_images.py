#!/usr/bin/env python3
"""
pdf_images.py - pull the embedded page scans out of a scanned PDF (JPEG/DCTDecode, or CCITT fax G3/G4
bitonal scans as used by many library digitisations). Reads the PDF as DATA only: nothing in the file is
executed or rendered by a PDF engine. CCITT pages are decoded with Pillow (libtiff) and re-saved as JPEG.

    python3 -E -P src/pdf_images.py <file.pdf> <out_dir> [--min-width 1000]

Writes p001.jpg, p002.jpg ... in page order (one image per page: the largest on that page) and
index.tsv (page, file, width, height, bytes). Small images (logos, cover-sheet graphics) are skipped.
(-E -P rather than -I so that a user-site Pillow is importable; -P still keeps the script dir off sys.path.)
"""
import argparse
import io
import pathlib
import re
import struct
import sys


def jpeg_size(b):
    """(width, height) from the first SOF marker of a JPEG byte string, or (0, 0)."""
    i = 2
    while i + 9 < len(b):
        if b[i] != 0xFF:
            i += 1
            continue
        marker = b[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seglen = struct.unpack(">H", b[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", b[i + 5:i + 9])
            return w, h
        i += 2 + seglen
    return 0, 0


def ccitt_to_jpeg(raw, w, h, k, black_is_1, byte_align):
    """Wrap a CCITT G3/G4 stream in a minimal TIFF and decode it with Pillow; return JPEG bytes."""
    from PIL import Image, ImageOps  # user-site install; see module docstring
    compression = 4 if k < 0 else 3
    entries = [(256, 4, 1, w), (257, 4, 1, h), (258, 3, 1, 1), (259, 3, 1, compression),
               (262, 3, 1, 0 if black_is_1 else 1), (266, 3, 1, 1), (273, 4, 1, 0),
               (277, 3, 1, 1), (278, 4, 1, h), (279, 4, 1, len(raw))]
    if k > 0:
        entries.append((292, 4, 1, 1 | (4 if byte_align else 0)))  # T4Options: 2D coding (+ byte-aligned EOLs)
    elif k == 0 and byte_align:
        entries.append((292, 4, 1, 4))
    entries.sort()
    ifd_off = 8
    data_off = ifd_off + 2 + 12 * len(entries) + 4
    buf = bytearray(b"II*\x00" + struct.pack("<I", ifd_off) + struct.pack("<H", len(entries)))
    for tag, typ, cnt, val in entries:
        if tag == 273:
            val = data_off
        buf += struct.pack("<HHII", tag, typ, cnt, val)
    buf += b"\x00\x00\x00\x00" + raw
    img = Image.open(io.BytesIO(bytes(buf)))
    img.load()
    img = img.convert("L")
    # scans of paper are mostly white; if the decode came out mostly black the polarity flag lied - invert
    hist = img.histogram()
    if sum(hist[:128]) > sum(hist[128:]):
        img = ImageOps.invert(img)
    out = io.BytesIO()
    img.save(out, "JPEG", quality=80)
    return out.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--min-width", type=int, default=1000)
    a = ap.parse_args()
    data = pathlib.Path(a.pdf).read_bytes()
    if not data.startswith(b"%PDF"):
        sys.exit("not a PDF")

    # object table: number -> start of object body
    objs = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj\s*", data):
        objs.setdefault(int(m.group(1)), m.end())

    def obj_body(n):
        start = objs[n]
        end = data.find(b"endobj", start)
        return data[start:end if end > 0 else start + 2000]

    def length_of(d):
        m = re.search(rb"/Length\s+(\d+)\s+0\s+R", d)
        if m:
            return int(re.match(rb"\s*(\d+)", obj_body(int(m.group(1)))).group(1))
        return int(re.search(rb"/Length\s+(\d+)", d).group(1))

    def num(d, key, default):
        m = re.search(rb"/" + key + rb"\s+(-?\d+)", d)
        return int(m.group(1)) if m else default

    images = {}  # obj number -> (jpeg bytes, w, h)
    n_ccitt = 0
    for n, start in objs.items():
        head = data[start:start + 4000]
        si = head.find(b"stream")
        if si < 0:
            continue
        d = head[:si]
        if b"/Subtype" not in d or b"/Image" not in d:
            continue
        is_jpeg, is_ccitt = b"/DCTDecode" in d, b"/CCITTFaxDecode" in d
        if not (is_jpeg or is_ccitt):
            continue
        p = start + si + len(b"stream")
        if data[p:p + 2] == b"\r\n":
            p += 2
        elif data[p:p + 1] in (b"\n", b"\r"):
            p += 1
        try:
            ln = length_of(d)
        except Exception:
            continue
        raw = data[p:p + ln]
        if is_jpeg:
            if not raw.startswith(b"\xff\xd8"):
                continue
            w, h = jpeg_size(raw)
            images[n] = (raw, w, h)
        else:
            w, h = num(d, b"Width", 0), num(d, b"Height", 0)
            if w < a.min_width and h < a.min_width:
                continue
            parms = re.search(rb"/DecodeParms\s*<<(.*?)>>", d, re.S)
            pd = parms.group(1) if parms else b""
            k = num(pd, b"K", 0)
            black_is_1 = b"/BlackIs1 true" in pd
            byte_align = b"/EncodedByteAlign true" in pd
            try:
                images[n] = (ccitt_to_jpeg(raw, w, h, k, black_is_1, byte_align), w, h)
                n_ccitt += 1
            except Exception as e:  # noqa: BLE001
                print(f"CCITT decode failed for object {n}: {e}", file=sys.stderr)

    # page order: walk page objects in the order of the Pages tree (Kids arrays, depth-first)
    def kids(n):
        body = obj_body(n)
        m = re.search(rb"/Kids\s*\[(.*?)\]", body, re.S)
        if not m:
            return [n]
        out = []
        for k in re.findall(rb"(\d+)\s+0\s+R", m.group(1)):
            out += kids(int(k))
        return out

    cat = next((n for n in objs if re.search(rb"/Type\s*/Catalog", obj_body(n))), None)
    root_pages = int(re.search(rb"/Pages\s+(\d+)\s+0\s+R", obj_body(cat)).group(1))
    page_objs = kids(root_pages)

    out = pathlib.Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    pno = 0
    for pg in page_objs:
        body = obj_body(pg)
        res = re.search(rb"/Resources\s+(\d+)\s+0\s+R", body)
        resb = obj_body(int(res.group(1))) if res else body
        xo = re.search(rb"/XObject\s*<<(.*?)>>", resb, re.S)
        if not xo:
            xr = re.search(rb"/XObject\s+(\d+)\s+0\s+R", resb)
            xo_b = obj_body(int(xr.group(1))) if xr else b""
        else:
            xo_b = xo.group(1)
        cands = [images[int(k)] for k in re.findall(rb"/\w+\s+(\d+)\s+0\s+R", xo_b) if int(k) in images]
        if not cands:
            continue
        jpg, w, h = max(cands, key=lambda t: t[1] * t[2])
        if w < a.min_width and h < a.min_width:
            continue
        pno += 1
        name = f"p{pno:03d}.jpg"
        (out / name).write_bytes(jpg)
        rows.append(f"{pno}\t{name}\t{w}\t{h}\t{len(jpg)}")
    (out / "index.tsv").write_text("page\tfile\twidth\theight\tbytes\n" + "\n".join(rows) + "\n")
    print(f"{len(page_objs)} PDF pages, {pno} scan images written to {out} ({n_ccitt} CCITT decoded)")


if __name__ == "__main__":
    main()
