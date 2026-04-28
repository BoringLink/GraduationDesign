#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

DEFAULT_TIMEOUT = 30
DEFAULT_USER_AGENT = "codex-literature-search/1.0"


def compact_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.split())


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_url(base_url: str, params: dict[str, Any] | None = None) -> str:
    if not params:
        return base_url

    query_items: list[tuple[str, str]] = []
    for key, value in params.items():
        if value is None or value == "":
            continue
        if isinstance(value, (list, tuple)):
            for item in value:
                if item is not None and item != "":
                    query_items.append((key, str(item)))
            continue
        query_items.append((key, str(value)))

    if not query_items:
        return base_url

    return f"{base_url}?{urllib.parse.urlencode(query_items)}"


def make_headers(
    *,
    api_key: str | None = None,
    api_key_env: str | None = None,
    accept: str = "application/json",
    extra_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    headers = {
        "Accept": accept,
        "User-Agent": DEFAULT_USER_AGENT,
    }

    resolved_key = api_key
    if not resolved_key and api_key_env:
        resolved_key = os.environ.get(api_key_env)
    if resolved_key:
        headers["x-api-key"] = resolved_key

    if extra_headers:
        headers.update(extra_headers)

    return headers


def fetch_text(url: str, *, headers: dict[str, str] | None = None, timeout: int = DEFAULT_TIMEOUT) -> str:
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed for {url}: {exc.reason}") from exc


def fetch_json(url: str, *, headers: dict[str, str] | None = None, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    text = fetch_text(url, headers=headers, timeout=timeout)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse JSON response from {url}: {exc}") from exc


def post_json(
    url: str,
    payload: dict[str, Any],
    *,
    headers: dict[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=request_headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed for {url}: {exc.reason}") from exc


def emit_output(
    payload: dict[str, Any],
    *,
    output_path: str | None = None,
    output_format: str = "json",
    markdown_renderer: Callable[[dict[str, Any]], str] | None = None,
) -> None:
    if output_format == "json":
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    elif output_format == "markdown":
        if markdown_renderer is None:
            raise ValueError("markdown output requested but no renderer was provided")
        text = markdown_renderer(payload)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

    if not text.endswith("\n"):
        text += "\n"

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(text, encoding="utf-8")
        return

    sys.stdout.write(text)
