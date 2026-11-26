import json
import os
from pathlib import Path

CAP = 120


def read_entry():
    side = Path(__file__).resolve().parent / "entry.txt"
    data = side.read_bytes().decode("utf-8-sig")
    return " ".join(data.split())


def check(msg):
    size = len(msg)
    if size == 0 or size > CAP:
        raise ValueError("size %d outside 1..%d" % (size, CAP))
    return size


def publish(msg):
    zone = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    zone.mkdir(parents=True, exist_ok=True)
    slot = zone / "entry.txt"
    slot.write_bytes((msg + "\n").encode("utf-8"))
    return slot


def main():
    msg = read_entry()
    size = check(msg)
    slot = publish(msg)
    print(json.dumps({"valid": True, "bytes": len(msg.encode("utf-8")), "chars": size, "slot": str(slot)}))


if __name__ == "__main__":
    main()
