import pandas as pd

def main():
    df_map = pd.read_csv('dataFile/area_map.csv') # x, y, ConstructionSite
    df_struct = pd.read_csv('dataFile/area_struct.csv') # x, y, category, area
    df_category = pd.read_csv('dataFile/area_category.csv') # category,  공백struct
    # print(df_map.columns)
    # print(df_struct.columns)
    # print(df_category.columns)

    df_category.columns = [col.strip() for col in df_category.columns]

    
    df_struct = df_struct.merge(df_category, how='left', on='category')

    
    df_struct.drop(columns=['category'], inplace=True)
    df_struct.rename(columns={'struct': 'category'}, inplace=True)

    
    df_sorted = df_struct.sort_values(by='area')
    df_area1 = df_sorted[df_sorted['area'] == 1]

    
    print("area 1 구조물 데이터:")
    print(df_area1)

    print("\n구조물 종류별 개수:")
    print(df_area1['category'].value_counts())

    return df_area1

if __name__ == '__main__':
    df_filtered = main()
    df_filtered.to_csv('output/area1_structures.csv', index=False)