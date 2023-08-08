"""Tests specific to the molecule plugin functionality."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest


def test_molecule_collect() -> None:
    """Test pytest collection of molecule scenarios."""
    try:
        proc = subprocess.run(
            "pytest --molecule --collect-only",
            capture_output=True,
            shell=True,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(exc.stderr)

    assert proc.returncode == 0
    assert "test[delegated]" in proc.stdout


def test_molecule_disabled() -> None:
    """Ensure the lack of --molecule disables molecule support."""

    proc = subprocess.run(
        f"{sys.executable} -m pytest tests/fixtures/molecule/default/molecule.yml",
        capture_output=True,
        check=False,
        env={"PATH": os.environ["PATH"]},
        shell=True,
        text=True,
    )
    assert proc.returncode == 4
    assert "ERROR: found no collectors" in proc.stdout


def test_molecule_runtest() -> None:
    """Test running the molecule scenarion via pytest."""

    proc = subprocess.run(
        f"{sys.executable} -m pytest --molecule tests/fixtures/molecule/default/molecule.yml",
        capture_output=True,
        check=True,
        env={"PATH": os.environ["PATH"]},
        shell=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "collected 1 item" in proc.stdout
    assert "tests/fixtures/molecule/default/molecule.yml::test " in proc.stdout
    assert "1 passed" in proc.stdout