import os
import cv2
import numpy as np
import argparse
from pathlib import Path


def process_image(input_path, output_path, target_size=(512, 512)):
    """画像を透明部分でトリミングし、比率を維持しながら target_size にリサイズ"""
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)  # 透過情報も含めて読み込み
    if img is None:
        print(f"スキップ: {input_path}（画像を読み込めません）")
        return

    # 透過チャンネルがない場合はスキップ
    if img.shape[-1] != 4:
        print(f"スキップ: {input_path}（透過情報なし）")
        return

    alpha = img[:, :, 3]

    # ノイズ除去（しきい値処理で小さな点を除外）
    _, alpha_thresh = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(alpha_thresh)  # 非ゼロピクセルの座標を取得
    if coords is None:
        print(f"スキップ: {input_path}（透明画像？）")
        return

    # 透明部分をトリミング
    x, y, w, h = cv2.boundingRect(coords)
    trimmed = img[y : y + h, x : x + w]

    # 新しいサイズを計算（アスペクト比維持）
    h_ratio = target_size[1] / h
    w_ratio = target_size[0] / w
    scale = min(h_ratio, w_ratio)
    new_w, new_h = int(w * scale), int(h * scale)

    # 画像をリサイズ
    resized = cv2.resize(trimmed, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # 中央に配置するキャンバスを作成
    canvas = np.zeros((target_size[1], target_size[0], 4), dtype=np.uint8)
    y_offset = (target_size[1] - new_h) // 2
    x_offset = (target_size[0] - new_w) // 2

    # 画像を正しく中央に配置（X, Y方向のズレ修正）
    canvas[y_offset : y_offset + new_h, x_offset : x_offset + new_w] = resized

    # 出力ディレクトリ作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, canvas)
    print(f"処理完了: {output_path}")


def process_folder(input_folder, output_folder, target_size=(512, 512)):
    """指定フォルダ以下の画像をすべて処理して保存"""
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    for file in input_folder.rglob("*"):
        if file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            relative_path = file.relative_to(input_folder)
            output_path = output_folder / relative_path
            process_image(str(file), str(output_path), target_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="画像の透明部分をトリミングし、リサイズする"
    )
    parser.add_argument("input_dir", type=str, help="入力フォルダ")
    parser.add_argument("output_dir", type=str, help="出力フォルダ")
    parser.add_argument(
        "--size", type=int, nargs=2, default=[512, 512], help="出力画像サイズ (幅 高さ)"
    )
    args = parser.parse_args()

    process_folder(args.input_dir, args.output_dir, tuple(args.size))
