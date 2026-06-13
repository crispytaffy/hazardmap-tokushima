import csv
import json
import os

def csv_to_geojson(csv_file_path, geojson_file_path):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    if not os.path.exists(csv_file_path):
        print(f"Error: {csv_file_path} が見つかりません。")
        return

    print(f"変換を開始します: {csv_file_path}")
    success_count = 0
    skip_count = 0

    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                # ★現在の項目名 'lat', 'lng' に合わせて数値を読み込み
                lat = float(row['lat'])
                lon = float(row['lng'])
                
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat] # GeoJSONは [経度, 緯度] の順
                    },
                    "properties": {
                        # ★現在の項目名 'No.', '名称', '住所' に合わせて取得
                        "id": row.get('No.', ''),
                        "name": row.get('名称', '名称不明'),
                        "address": row.get('住所', '')
                    }
                }
                geojson['features'].append(feature)
                success_count += 1
                
            except (ValueError, KeyError) as e:
                # 緯度経度が空欄、または列名が合わないデータはスキップ
                skip_count += 1
                continue

    with open(geojson_file_path, mode='w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
        
    print(f"変換完了！ 成功: {success_count}件 / スキップ: {skip_count}件")

# 実行（ファイル名は実際のファイル名に合わせてください）
csv_to_geojson('toilet_list.csv', 'toilet_list.geojson')
