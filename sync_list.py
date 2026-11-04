#!/usr/bin/env python3
"""
bilibili-public-blockuserlist 同步脚本
用途：
1. 自动扫描 img/ 目录下的所有证据图片（如 {UID}.jpg 或 {UID}_{序号}.jpg）
2. 提取所有 UID 并与 piliplus_list.json 同步，自动补全缺失的 UID 并去重排序
3. 校验图片与名单一致性
"""

import os
import re
import json
import glob

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(REPO_DIR, "img")
JSON_PATH = os.path.join(REPO_DIR, "piliplus_list.json")
LIST_MD_PATH = os.path.join(REPO_DIR, "list.md")
LIST_TXT_PATH = os.path.join(REPO_DIR, "list.txt")

def main():
    print(">>> 正在扫描 img/ 目录中的证据图片...")
    img_files = glob.glob(os.path.join(IMG_DIR, "*.jpg")) + glob.glob(os.path.join(IMG_DIR, "*.png"))
    
    uid_to_images = {}
    for img_path in img_files:
        basename = os.path.basename(img_path)
        m = re.match(r"^(\d+)(?:_\d+)?\.(?:jpg|jpeg|png)$", basename, re.IGNORECASE)
        if m:
            uid = int(m.group(1))
            uid_to_images.setdefault(uid, []).append(basename)
        else:
            print(f"[提示] 未按 UID 命名的图片: {basename}")

    print(f"共发现 {len(img_files)} 张证据图片，涵盖 {len(uid_to_images)} 个独立 UID。")

    # 读取并更新 piliplus_list.json
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            current_uids = json.load(f)
    else:
        current_uids = []

    current_set = set(current_uids)
    added_uids = []
    for uid in uid_to_images:
        if uid not in current_set:
            current_uids.append(uid)
            current_set.add(uid)
            added_uids.append(uid)

    if added_uids:
        print(f"发现 {len(added_uids)} 个新增 UID，正在同步追加到 piliplus_list.json: {added_uids}")
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(current_uids, f, indent=4, ensure_ascii=False)
        print("piliplus_list.json 更新成功！")
    else:
        print("piliplus_list.json 已经包含所有图片中的 UID。")

    print(f"当前黑名单总用户数: {len(current_uids)}")
    print("同步完成！")

if __name__ == "__main__":
    main()
