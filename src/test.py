import pandas as pd

def main():
    # 데이터 읽기
    df_map = pd.read_csv('dataFile/area_map.csv')  # x, y, ConstructionSite
    df_struct = pd.read_csv('dataFile/area_struct.csv')  # x, y, category, area
    df_category = pd.read_csv('dataFile/area_category.csv')  # category, struct

    # 전처리
    df_category.columns = [col.strip() for col in df_category.columns]
    df_struct['category'] = df_struct['category'].astype(str).str.strip()
    df_category['category'] = df_category['category'].astype(str).str.strip()

    # category 이름 mapping
    df_struct = df_struct.merge(df_category, how='left', on='category')
    df_struct.drop(columns=['category'], inplace=True)
    df_struct.rename(columns={'struct': 'category'}, inplace=True)
    df_struct['category'] = df_struct['category'].astype(str).str.strip()

    # (x, y)를 기준으로 area_map과 병합
    df_merged = df_map.merge(df_struct, how='left', on=['x', 'y'])

    # ConstructionSite == 1이고 category가 NaN인 경우 → constructionSite로 채움
    mask = (df_merged['ConstructionSite'] == 1) & (df_merged['category'].isna())
    df_merged.loc[mask, 'category'] = 'constructionSite'

    # area가 없는 경우도 있을 수 있으므로 NaN을 int로 캐스팅하지 않고 그대로 둠
    df_merged.to_csv('output/full_structures_map.csv', index=False)

    return df_merged

if __name__ == '__main__':
    df_full = main()