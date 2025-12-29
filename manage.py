"""Unified launcher for all weather app variants."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parent

APP_DEFINITIONS: Dict[str, Dict[str, object]] = {
    "basic-cli": {
        "module": "src.apps.basic_terminal",
        "description": " basic terminal app",
    },
    "advanced-cli": {
        "module": "src.apps.advanced_terminal",
        "description": " Rich formatting + multiple cities",
    },
    "cli": {
        "module": "src.apps.cli",
        "description": " argparse-based CLI",
    },
    "geolocation": {
        "module": "src.apps.geolocation_app",
        "description": " auto-detect location + forecast",
    },
    "voice": {
        "module": "src.apps.voice_app",
        "description": " speech input/output",
    },
    "ai-assistant": {
        "module": "src.apps.ai_assistant",
        "description": " OpenAI powered tips",
        "needs_openai": True,
    },
    "tkinter": {
        "module": "src.apps.tkinter_app",
        "description": " Tkinter GUI",
    },
    "pyqt": {
        "module": "src.apps.pyqt_app",
        "description": " PyQt5 GUI",
    },
    "flask": {
        "module": "src.apps.flask_app",
        "description": " Flask frontend/backend",
    },
    "fastapi": {
        "module": "src.apps.fastapi_service",
        "description": " FastAPI microservice",
    },
}


def ensure_env(meta: Dict[str, object]) -> None:
    """Fail fast if required API keys are missing."""

    sys.path.insert(0, str(PROJECT_ROOT))
    from src.config.settings import get_settings

    settings = get_settings()
    if not settings.has_openweather_key:
        raise SystemExit(
            "OPENWEATHER_API_KEY is missing. Set it in .env or environment variables."
        )
    if meta.get("needs_openai") and not settings.has_openai_key:
        raise SystemExit(
            "This app needs OPENAI_API_KEY. Set it in .env before running."
        )


def run_app(name: str, extra_args: list[str]) -> int:
    meta = APP_DEFINITIONS[name]
    ensure_env(meta)

    module = meta["module"]
    cmd = [sys.executable, "-m", module, *extra_args]
    process = subprocess.run(cmd, cwd=PROJECT_ROOT)
    return process.returncode


def interactive_menu() -> int:
    names = list(APP_DEFINITIONS.keys())
    while True:
        print("\n=== Weather Project Launcher ===")
        for idx, key in enumerate(names, start=1):
            print(f"{idx}. {key:<12} – {APP_DEFINITIONS[key]['description']}")
        print("Q. Quit")

        choice = input("Select an app to run: ").strip().lower()
        if choice in {"q", "quit", "exit"}:
            return 0
        if not choice.isdigit():
            print("Please enter a number from the list.")
            continue
        idx = int(choice) - 1
        if idx < 0 or idx >= len(names):
            print("Invalid option. Try again.")
            continue
        name = names[idx]
        print(f"\nLaunching {name}... Press Ctrl+C to stop.")
        try:
            returncode = run_app(name, [])
        except SystemExit as exc:
            print(str(exc))
            continue
        if returncode != 0:
            print(f"App exited with code {returncode}.")
        else:
            print("App exited successfully.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run any of the weather app variants from a single entry point."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all available app targets")
    subparsers.add_parser("menu", help="Show interactive menu to launch apps")

    run_parser = subparsers.add_parser("run", help="Run a specific app target")
    run_parser.add_argument("app", choices=APP_DEFINITIONS.keys())
    run_parser.add_argument(
        "app_args",
        nargs=argparse.REMAINDER,
        help="Additional args passed to the underlying app (prefix with --)",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "list":
        for name, meta in APP_DEFINITIONS.items():
            print(f"{name:<12} {meta['description']}")
        return 0
    if args.command == "menu":
        return interactive_menu()
    if args.command == "run":
        try:
            return run_app(args.app, args.app_args or [])
        except SystemExit as exc:
            print(str(exc))
            return 1
    raise SystemExit("Unknown command")


if __name__ == "__main__":
    import os
    
    if os.environ.get("RENDER"):
        # Non-interactive environment → run Flask instead of menu
        from app import app
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        # Local interactive menu
        main()



                    
