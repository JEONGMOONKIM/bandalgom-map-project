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

    df_struct = df_struct.merge(df_map, how='left', on=['x', 'y']) #ConstructionSite 정보 merge
    #ConstructionSite == 1 and category is nan → 'ConstructionSite'로 대체
    mask = (df_struct['ConstructionSite'] == 1) & (df_struct['category'].str.lower() == 'nan') 
    df_struct.loc[mask, 'category'] = 'ConstructionSite'
    
    df_struct.drop(columns=['ConstructionSite'], inplace=True)



    df_area12 = df_struct[df_struct['area'].isin([1, 2])] #'Myhome'이 포함된건 area2이므로 저장은 area1,2
    df_area1 = df_struct[df_struct['area']==1] # 과제1에서 area1에 대해서만 출력을 요구

    
    print("area 1 구조물 데이터:")
    print(df_area1)

    print("\n구조물 종류별 개수:")
    print(df_area1['category'].value_counts())

    return df_area12

if __name__ == '__main__':
    df_filtered = main()
    df_filtered.to_csv('output/area12_structures.csv', index=False)