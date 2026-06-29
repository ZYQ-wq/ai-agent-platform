import time
import urllib.error
import urllib.request

import docker
import socket

client = docker.from_env()


class SandboxService:

    @staticmethod
    def get_free_port():

        s = socket.socket()

        s.bind(("", 0))

        port = s.getsockname()[1]

        s.close()

        return port

    @staticmethod
    def run_python(
        workdir: str,
        entry_file:str ="main.py"
    ):
        container = client.containers.run(
            image="python:3.11-slim",

            command=f"python {entry_file}",

            working_dir="/workspace",

            volumes={
                workdir: {
                    "bind": "/workspace",
                    "mode": "ro"
                }
            },

            network_disabled=True,

            mem_limit="256m",

            nano_cpus=500000000,

            pids_limit=64,

            detach=True,

            remove=False,

            read_only=True,

            user="1000:1000",

        )

        result = container.wait(timeout=15)

        logs = container.logs().decode()

        container.remove(force=True)

        return {
            "success": result["StatusCode"] == 0,
            "logs": logs
        }
    
    @staticmethod
    def _wait_for_http(port: int, path: str = "/", timeout: float = 10.0):
        url = f"http://127.0.0.1:{port}{path}"
        deadline = time.time() + timeout

        while time.time() < deadline:
            try:
                with urllib.request.urlopen(url, timeout=1) as response:
                    if response.status == 200:
                        return
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                time.sleep(0.2)

        raise RuntimeError(
            f"预览服务启动超时: {url}"
        )

    @staticmethod
    def run_web(
        workdir: str,
        entry_path: str = "index.html"
    ):

        port = SandboxService.get_free_port()
        preview_path = entry_path.replace("\\", "/").lstrip("/")

        container = client.containers.run(
            image="python:3.11-slim",

            command="python -m http.server 8000 --bind 0.0.0.0",

            working_dir="/workspace",

            volumes={
                workdir: {
                    "bind": "/workspace",
                    "mode": "ro"
                }
            },

            ports={
                "8000/tcp": ("127.0.0.1", port)
            },

            network_disabled=False,

            detach=True,

            remove=False
        )

        SandboxService._wait_for_http(
            port,
            f"/{preview_path}"
        )

        return {
            "success": True,
            "preview_url":
                f"http://127.0.0.1:{port}/{preview_path}",
            "container_id":
                container.id
        }

    @staticmethod
    def stop_container(container_id: str):
        try:
            container = client.containers.get(container_id)
            container.stop(timeout=3)
            container.remove(force=True)
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError:
            pass

