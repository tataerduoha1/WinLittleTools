import bencodepy
import os

def dump_torrent_file_names(torrent_path, output_txt):
    with open(torrent_path, "rb") as f:
        raw_data = f.read()
    data = bencodepy.decode(raw_data)

    files_info = data.get(b"info", {})
    file_list = []

    # 单文件种子
    if b"length" in files_info:
        name = files_info[b"name"].decode("utf-8", errors="replace")
        file_list.append(name)
    # 多文件种子
    elif b"files" in files_info:
        base_name = files_info[b"name"].decode("utf-8", errors="replace")
        for item in files_info[b"files"]:
            path_parts = [p.decode("utf-8", errors="replace") for p in item[b"path"]]
            full_path = os.path.join(base_name, *path_parts)
            file_list.append(full_path)

    with open(output_txt, "w", encoding="utf-8") as out:
        for line in file_list:
            out.write(line + "\n")

    print(f"已导出 {len(file_list)} 个文件名，保存至：{output_txt}")

if __name__ == "__main__":
    # -------------------修改这里----------------
    TORRENT_FILE = r"test.torrent"
    OUTPUT = r"file_names.txt"
    # -------------------------------------------
    dump_torrent_file_names(TORRENT_FILE, OUTPUT)
