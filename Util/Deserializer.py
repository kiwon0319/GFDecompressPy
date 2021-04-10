import unitypack

def deserialize(_file_path, _file_name):
  with open(_file_path, "rb") as f:
    bundle = unitypack.load(f)


  for asset in bundle.assets:
    for id, object in asset.objects.items():
      if object.type == "AssetBundleDataObject":
        data = object.read() # 해당 위치에서 시간지연 발생. 문제 확인 후 수정요망
        resurl = data["resUrl"]
        for key, value in enumerate(data["BaseAssetBundles"]):
          if value["assetBundleName"] == _file_name:
            resname = value["resname"]
            return [resurl, resname]