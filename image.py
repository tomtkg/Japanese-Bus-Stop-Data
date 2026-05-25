import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, to_hex
from japanmap import picture
from prefectures import PREF_POS

def save_image(name: str, dic: dict[int, int]) -> None:
    bbox = dict(facecolor='white', alpha=.5, edgecolor='none', pad=0)
    cmap = plt.get_cmap("Reds")
    norm = Normalize(min(dic.values()), max(dic.values()))
    
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(picture({k: to_hex(cmap(norm(v))) for k, v in dic.items()}))
    for k, v in dic.items():
        plt.text(*PREF_POS[k], str(v), ha='center', va='center', bbox=bbox)
    plt.savefig("images/"+name, dpi=600, bbox_inches='tight', pad_inches=0)
