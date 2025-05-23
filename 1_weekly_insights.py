import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date, timedelta

# === 設定 ===
target_name = 'person'
target_direction = 'toNorth'
csv_path = 'kajibashichushajo.csv'

# === データ読み込みと加工 ===
df = pd.read_csv(csv_path, parse_dates=['datetime_jst'])
df['year'] = df['datetime_jst'].dt.year
df['week'] = df['datetime_jst'].dt.isocalendar().week
df['hour'] = df['datetime_jst'].dt.strftime('%H:%M')
df['dayofweek'] = df['datetime_jst'].dt.dayofweek  # 0=Monday, ..., 6=Sunday

# 曜日番号 → 名称
weekday_map = {
    0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
    4: 'Friday', 5: 'Saturday', 6: 'Sunday'
}

# === フィルター ===
df_filtered = df[
    (df['name'] == target_name) &
    (df['countingDirection'] == target_direction)
]

# === 出力フォルダ作成 ===
output_dir = 'weekly_graphs_by_year'
csv_output_dir = 'weekly_csv_by_year'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(csv_output_dir, exist_ok=True)

# === 年 × 週 ごとのグラフ作成とCSV出力 ===
for year in sorted(df_filtered['year'].unique()):
    df_year_all = df_filtered[df_filtered['year'] == year]

    for week in range(1, 49):
        df_week = df_year_all[df_year_all['week'] == week]

        if df_week.empty:
            print(f"{year}年 {week}週：データなし")
            continue

        # ピボット：dayofweek × 時間
        pivot_df = df_week.groupby(['dayofweek', 'hour'])['count_1_hour'].sum().unstack(level=0).fillna(0)

        # 存在する曜日だけ選ぶ
        existing_days = [d for d in range(7) if d in pivot_df.columns]

        if not existing_days:
            print(f"{year}年 {week}週：曜日データなし")
            continue

        # === ピボットを曜日名に変換してCSV保存 ===
        pivot_df_renamed = pivot_df.rename(columns=weekday_map)
        csv_filename = f"{csv_output_dir}/{year}_week_{week:02d}_{target_name}.csv"
        pivot_df_renamed.to_csv(csv_filename, encoding='utf-8-sig')
        print(f"{year}年 {week}週：CSV保存完了 → {csv_filename}")

        # === グラフ描画 ===
        plt.figure(figsize=(16, 8))
        for d in existing_days:
            plt.plot(
                pivot_df.index,
                pivot_df[d],
                label=weekday_map[d],
                marker='o'
            )

        # === 週の解析日付範囲（ISOカレンダー：月曜始まり） ===
        try:
            start_date = date.fromisocalendar(year, week, 1)
            end_date = start_date + timedelta(days=6)
            date_range_str = f"{start_date.strftime('%Y/%m/%d')} - {end_date.strftime('%Y/%m/%d')}"
        except ValueError:
            date_range_str = "Invalid date range"

        # === タイトルに週範囲を含める ===
        plt.title(f"{target_name} - {target_direction} | {year} Week {week} ({date_range_str})\nHourly Trends by Weekday")
        plt.xlabel("Hour")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend(ncol=2)
        plt.tight_layout()

        filename_graph = f"{output_dir}/{year}_week_{week:02d}_{target_name}.png"
        plt.savefig(filename_graph)
        plt.close()

        print(f"{year}年 {week}週：グラフ保存完了 → {filename_graph}")
