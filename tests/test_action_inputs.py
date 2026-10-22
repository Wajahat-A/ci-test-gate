"""Regression tests for the ci-test-gate GitHub Action (action.yml).

The `test-files-list` input was declared but never forwarded to the CLI, so
every Action run classified zero known tests and the gate recommendation was
useless for Action users (issue #104). These tests are deliberately static:
they parse action.yml itself and assert each declared input is actually
consumed by the run steps, so the wiring cannot silently rot again.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ACTION = Path(__file__).resolve().parents[1] / "action.yml"


@pytest.fixture(scope="module")
def action() -> dict:
    assert ACTION.is_file(), f"action.yml not present at {ACTION}"
    return yaml.safe_load(ACTION.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def run_text(action: dict) -> str:
    steps = action["runs"]["steps"]
    run_blocks = [s.get("run", "") for s in steps if "run" in s]
    assert run_blocks, "action.yml has no run steps"
    return "\n".join(run_blocks)


def test_test_files_list_input_is_forwarded(action: dict, run_text: str):
    assert "test-files-list" in action["inputs"], "input declaration missing"
    assert "test-files-list" in run_text, (
        "test-files-list input is declared but never referenced in run steps"
    )
    assert "--test-files" in run_text, (
        "run steps never pass --test-files to the CLI"
    )


def test_diff_file_input_is_forwarded(action: dict, run_text: str):
    assert "diff-file" in action["inputs"], "input declaration missing"
    assert "diff-file" in run_text
    assert "--diff" in run_text


def test_mode_input_is_forwarded(action: dict, run_text: str):
    assert "mode" in action["inputs"], "input declaration missing"
    assert "inputs.mode" in run_text
