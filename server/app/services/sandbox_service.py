import docker

client = docker.from_env()


class SandboxService:

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
    def run_web(
        workdir: str
    ):

        return {
            "success": True,
            "logs":
                "检测到Web项目\n"
                "当前版本暂不支持浏览器预览\n"
                "请后续实现 Web Preview"
        }