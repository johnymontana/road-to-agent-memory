"""Exercise the dev launcher's command dispatch, failure handling, and cleanup."""

import os
import signal
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def launcher_env(tmp_path):
    executable = tmp_path / "service"
    executable.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, signal, sys, time\n"
        "root = pathlib.Path(os.environ['LAUNCHER_TEST_DIR'])\n"
        "name = pathlib.Path(sys.argv[0]).name\n"
        "if name == 'uv' and sys.argv[1:] == ['run', 'python', '-']:\n"
        "    sys.stdin.read()\n"
        "    if os.environ.get('BUSY_PORT'):\n"
        "        print('Port 8000 is already in use.', flush=True)\n"
        "        sys.exit(1)\n"
        "    sys.exit(0)\n"
        "if name == 'npm' and sys.argv[1:5] != ['--prefix', 'web', 'run', 'dev']:\n"
        "    print('Unknown command: dev', flush=True)\n"
        "    sys.exit(1)\n"
        "(root / (name + '.pid')).write_text(str(os.getpid()))\n"
        "if name == os.environ.get('FAIL_SERVICE', 'npm'):\n"
        "    time.sleep(0.2)\n"
        "    sys.exit(37)\n"
        "while True: time.sleep(1)\n"
    )
    executable.chmod(0o755)
    for name in ("uv", "npm"):
        (tmp_path / name).symlink_to(executable)
    return {
        **os.environ,
        "PATH": f"{tmp_path}:{os.environ['PATH']}",
        "LAUNCHER_TEST_DIR": str(tmp_path),
    }


def run_launcher(env):
    process = subprocess.Popen(
        ["bash", "scripts/dev.sh"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        output, _ = process.communicate()
        pytest.fail(f"Launcher did not stop after a service failed:\n{output}")
    return process.returncode, output


@pytest.mark.parametrize("failed_service", ["uv", "npm"])
def test_service_failure_stops_the_other_service(launcher_env, failed_service):
    launcher_env["FAIL_SERVICE"] = failed_service
    code, output = run_launcher(launcher_env)
    assert "Unknown command" not in output
    assert code == 37, output
    for name in ("uv", "npm"):
        pid_file = Path(launcher_env["LAUNCHER_TEST_DIR"]) / f"{name}.pid"
        assert pid_file.exists(), f"{name} was not started: {output}"
        with pytest.raises(ProcessLookupError):
            os.kill(int(pid_file.read_text()), 0)


def test_busy_port_prevents_both_services_from_starting(launcher_env):
    launcher_env["BUSY_PORT"] = "1"
    code, output = run_launcher(launcher_env)
    assert code != 0
    assert "Port 8000 is already in use" in output
    assert not list(Path(launcher_env["LAUNCHER_TEST_DIR"]).glob("*.pid"))
