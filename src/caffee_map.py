import pandas as pd

def main():
    df_map = pd.read_csv('dataFile/area_map.csv') # x, y, ConstructionSite
    df_struct = pd.read_csv('dataFile/area_struct.csv') # x, y, category, area
    df_category = pd.read_csv('dataFile/area_category.csv') # category,  공백struct
    # print(df_map.columns)
    # print(df_struct.columns)
    # print(df_category.columns)

    df_category.columns = [col.strip() for col in df_category.columns] #컬럼 이름 공백 제거
    
    df_struct['category'] = df_struct['category'].astype(str).str.strip() #셀 내부 문자열 공백 제거
    df_category['category'] = df_category['category'].astype(str).str.strip()


    df_struct = df_struct.merge(df_category, how='left', on='category') #df_struct의 category 기준으로 df_category와 left join
    df_struct.drop(columns=['category'], inplace=True) # 원본 반영 inplace=True
    df_struct.rename(columns={'struct': 'category'}, inplace=True)
    df_struct['category'] = df_struct['category'].astype(str).str.strip()

    df_area12 = df_struct[df_struct['area'].isin([1, 2])]
    # df_area1 = df_struct[df_struct['area']==1]
    # df_sorted = df_struct.sort_values(by='area') # 정렬이 필요할 경우 사용
    # df_area1 = df_sorted[df_sorted['area'] == 1]  
    
    print("area 1 구조물 데이터:")
    print(df_area12)

    print("\n구조물 종류별 개수:")
    print(df_area12['category'].value_counts())

    return df_area12

if __name__ == '__main__':
    df_filtered = main()
    df_filtered.to_csv('output/area12_structures.csv', index=False)