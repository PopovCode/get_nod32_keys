import os


def clear_tmp_folder():
    tmp_path = "tmp/"
    tmp_files = os.listdir(tmp_path)
    for tmp_f in tmp_files:
        os.remove(os.path.join(tmp_path, tmp_f))
    print('[INFO] - Temp folder is cleaning.... OK!')
