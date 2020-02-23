from pycocotools.coco import COCO

anno_path = "/home/sakamoto/Downloads/annotations/instances_train2014.json"
coco = COCO(anno_path)

# カテゴリ ID の一覧を取得する。
cat_names = ["person", "bicycle", "car", "motorcycle", "bus", "truck"]

cat_ids = [0,0,0,0,0,0]
for i in range(6):
  cat_ids[i] = coco.getCatIds(catNms=[cat_names[i]])


# 指定したカテゴリ ID の物体がすべて存在する画像の ID 一覧を取得する。
img_ids = [0,0,0,0,0,0]
for i in range(6):
  img_ids[i] = coco.getImgIds(catIds=cat_ids[i])
print(img_ids)  # [338624, 424162, 407083, 67213, 421455, 395801, 151962, 139099, 324158]

from pathlib import Path
import PIL.Image
import PIL.ImageDraw
import os

#for i in range(6):
i=5
print("img_ids="+str(img_ids))
for id in img_ids[i]:
  print(id)
  img_id = id

  # 指定した画像 ID に対応する画像の情報を取得する。
  img_info, = coco.loadImgs(img_id)
  img_path = Path("/home/sakamoto/Downloads/train2014") / img_info["file_name"]
  print(img_path)  # /data/train2017/000000494089.jpg

  # 指定した 画像 ID に対応するアノテーション ID を取得する。
  anno_ids = coco.getAnnIds(img_id)

  # 指定したアノテーション ID に対応するアノテーションの情報を取得する。
  annos = coco.loadAnns(anno_ids)

  # 画像を読み込む。
  image = PIL.Image.open(img_path).convert('RGB')
  draw = PIL.ImageDraw.Draw(image)

  for anno in annos:
  
    try:
      category_id = anno["category_id"]
      cat_id = cat_ids[i]
      if cat_id[0] != category_id:
        continue
      data = anno["bbox"]
      xy = (data[0], data[1], data[0]+data[2], data[1]+data[3])

      draw.rectangle(xy, outline=(255, 0, 0), width=3)
    except ZeroDivisionError:
      pass
  dir = "/home/sakamoto/vis_coco/" + str(cat_names[i])
  if not os.path.isdir(dir):
    os.makedirs(dir)
  image.save(dir + "/" + str(id) + ".png")


  # アノテーション結果を描画する。
  #coco.showAnns(annos)
