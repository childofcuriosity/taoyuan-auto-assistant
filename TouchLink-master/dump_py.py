import os

# ===== 黑名单配置 =====
BLACKLIST_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
}

BLACKLIST_FILES = {
    "__init__.py",
    "dump_py.py",
}

BLACKLIST_SUFFIXES = {
    ".pyc",
    ".jar"
}
# =====================


def dump_py_files(root_dir, output_file):
    with open(output_file, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk(root_dir):

            # 目录黑名单（关键：直接修改 dirs）
            dirs[:] = [d for d in dirs if d not in BLACKLIST_DIRS]

            for name in files:
                # 文件名黑名单
                if name in BLACKLIST_FILES:
                    continue

                # 后缀黑名单
                if any(name.endswith(s) for s in BLACKLIST_SUFFIXES):
                    continue


                file_path = os.path.join(root, name)
                out.write(f"\n===== {file_path} =====\n\n")

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        out.write(f.read())
                        out.write("\n")
                except UnicodeDecodeError:
                    out.write("[无法用 utf-8 解码该文件]\n")


if __name__ == "__main__":
    dump_py_files(".", "all_py_dump.txt")
