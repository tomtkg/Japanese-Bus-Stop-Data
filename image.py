import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, to_hex
from japanmap import picture
from prefecture import PREF_POS

def save_image(name: str, vec: list[int]) -> None:
    file_name = "images/"+name+".png"
    bbox = dict(facecolor='white', alpha=.5, edgecolor='none', pad=0)
    cmap = plt.get_cmap("Reds")
    norm = Normalize(min(vec), max(vec))
    img = picture({k: to_hex(cmap(norm(v))) for k, v in enumerate(vec, 1)})

    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(img)  # type: ignore
    for k, v in enumerate(vec, 1):
        plt.text(*PREF_POS[k], str(v), ha='center', va='center', bbox=bbox)
    plt.savefig(file_name, dpi=600, bbox_inches='tight', pad_inches=0)
    
    
