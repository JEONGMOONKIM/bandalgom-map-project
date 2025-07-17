import pandas as pd
import matplotlib.pyplot as plt

def main():
    df_struct = pd.read_csv('output/area12_structures.csv')
    # df_struct = pd.read_csv('output/area1_structures.csv')
    df_map = pd.read_csv('dataFile/area_map.csv')
    
    df_struct['category'] = df_struct['category'].astype(str).str.strip()
    
    df_map['ConstructionSite'] = df_map['ConstructionSite'].astype(str).str.strip()
    construction_coords = df_map[df_map['ConstructionSite'] == '1'][['x', 'y']]
    construction_set = set([tuple(row) for row in construction_coords.to_numpy()])

    
    fig, ax = plt.subplots(figsize=(10, 10))

    
    max_x = max(df_struct['x'].max(), df_map['x'].max())
    max_y = max(df_struct['y'].max(), df_map['y'].max())

    for x in range(1, max_x + 2):
        ax.axvline(x - 0.5, color='lightgray', linewidth=0.5)
    for y in range(1, max_y + 2):
        ax.axhline(y - 0.5, color='lightgray', linewidth=0.5)
    
   
    category_map = {'Apartment': '아파트', 'Building': '빌딩', 
                    'BandalgomCoffee': '반달곰 커피', 'MyHome': '내 집'}
    df_struct['category'] = df_struct['category'].map(category_map).fillna('')
    
    
    for _, row in df_struct.iterrows():
        x, y, category = row['x'], row['y'], row['category']
        is_construction = (x, y) in construction_set

        if category == '내 집':
            ax.plot(x, y, marker='^', color='green', markersize=12)
        elif is_construction:
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray'))
        elif category in ['아파트', '빌딩']:
            ax.plot(x, y, 'o', color='brown', markersize=10)
        elif category == '반달곰 커피':
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='green'))
    
    
    handles = [
        plt.Line2D([], [], marker='o', color='w', label='아파트/빌딩', markerfacecolor='brown', markersize=10),
        plt.Line2D([], [], marker='s', color='w', label='반달곰 커피', markerfacecolor='green', markersize=10),
        plt.Line2D([], [], marker='^', color='w', label='내 집', markerfacecolor='green', markersize=10),
        plt.Rectangle((0,0), 1, 1, color='gray', label='건설 현장')
    ]
    ax.legend(handles=handles, loc='lower right')

    
    ax.set_xlim(0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, 0.5)
    ax.set_xticks(range(1, max_x + 1))
    ax.set_yticks(range(1, max_y + 1))
    ax.set_aspect('equal')

    
    plt.title("반달곰 커피 주변 지도")
    plt.grid(False)
    # plt.savefig('output/map1.png')
    plt.savefig('output/map12.png')
    plt.close()

if __name__ == '__main__':
    main()