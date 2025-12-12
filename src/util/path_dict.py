from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent

path_dic = {
    "log_config": project_dir.joinpath("config").joinpath("log_config.json")
}