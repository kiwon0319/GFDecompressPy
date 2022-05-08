# -*-coding:utf-8-*-
import UnityPy
import os


def unapck_all_asset(src_folder: str, dest_folder: str):
    for root, dirs, files in os.walk(src_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            env = UnityPy.load(file_path)

            for path, obj in env.container.items():
                if obj.type.name in ["Texture2D", "Sprite"]:
                    data = obj.read()

                    dest = os.path.join(dest_folder, *path.split("/"))

                    os.makedirs(os.path.dirname(dest), exist_ok=True)

                    dest, ext = os.path.splitext(dest)
                    dest += ".png"
                    data.image.save(dest)

                if obj.type.name == "TextAsset":
                    data = obj.read()

                    dest = os.path.join(dest_folder, *path.split("/"))

                    os.makedirs(os.path.dirname(dest), exist_ok=True)

                    dest, ext = os.path.splitext(dest)
                    dest += ".txt"
                    with open(dest, "wb") as f:
                        f.write(bytes(data.script))


def unpack_asset_filtered(src_path: str, dest_path: str, filter_list: list):
    env = UnityPy.load(src_path)
    os.makedirs(dest_path, exist_ok=True)

    for obj in env.objects:
        if obj.type.name in ["Texture2D", "Sprite"]:
            data = obj.read()

            if data.name in filter_list:
                dest = os.path.join(dest_path, data.name)
                dest = os.path.splitext(dest)
                dest += ".png"

                data.image.save(dest)

        if obj.type.name == "TextAsset":
            data = obj.read()

            if data.name in filter_list:
                dest = dest_path + "/" + data.name
                dest, ext = os.path.splitext(dest)
                dest += ".txt"

                with open(dest, "wb") as f:
                    f.write(bytes(data.script))
