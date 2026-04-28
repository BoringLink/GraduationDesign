import json
import statistics
import time
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar


def p95(values: list[float]) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    k = int(round(0.95 * (len(values) - 1)))
    return values[k]


def sample(name: str, fn, n: int = 200) -> dict:
    samples_ms: list[float] = []
    ok = 0
    for _ in range(n):
        t0 = time.perf_counter()
        status_code = fn()
        samples_ms.append((time.perf_counter() - t0) * 1000)
        if 200 <= status_code < 400:
            ok += 1
    return {
        "name": name,
        "n": n,
        "ok": ok,
        "error": n - ok,
        "avg_ms": round(statistics.mean(samples_ms), 3),
        "p95_ms": round(p95(samples_ms), 3),
        "max_ms": round(max(samples_ms), 3),
    }


def main():
    base = "https://codingplatform.mgsai.cn/api"
    out_path = "api_perf_cloud.json"

    jar = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    # login (set-cookie -> cookiejar)
    login_data = urllib.parse.urlencode({"username": "123", "password": "any"}).encode(
        "utf-8"
    )
    login_req = urllib.request.Request(
        f"{base}/users/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with opener.open(login_req, timeout=10) as resp:
        _ = resp.read()

    def get(path: str) -> int:
        req = urllib.request.Request(f"{base}{path}", method="GET")
        with opener.open(req, timeout=10) as resp:
            _ = resp.read()
            return resp.status

    def post_json(path: str, payload: dict) -> int:
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{base}{path}",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener.open(req, timeout=10) as resp:
            _ = resp.read()
            return resp.status

    res = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "base": base,
        "endpoints": [
            sample("GET /health", lambda: get("/health")),
            sample("GET /users/check", lambda: get("/users/check")),
            sample(
                "POST /platform/run (print)",
                lambda: post_json("/platform/run", {"code": "print(1+1)", "input_data": None}),
            ),
        ],
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

