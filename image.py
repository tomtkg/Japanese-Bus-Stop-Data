import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, to_hex
from japanmap import picture
from prefecture import PREF_JP, PREF_POS

def save_image(name: str, vec: list[int]) -> None:
    file_name = 'images/'+name+'.png'
    bbox = dict(facecolor='white', alpha=.5, edgecolor='none', pad=0)
    cmap = plt.get_cmap('Reds')
    norm = Normalize(min(vec), max(vec))
    img = picture({k: to_hex(cmap(norm(v))) for k, v in enumerate(vec, 1)})

    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(img)  # type: ignore
    for k, v in enumerate(vec, 1):
        plt.text(*PREF_POS[k], str(v), ha='center', va='center', bbox=bbox)
    plt.savefig(file_name, dpi=600, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    bar_name = 'images/'+name+'_bar.png'
    values = sorted(
        (("\n".join(PREF_JP[k][:3]), v) for k, v in enumerate(vec, 1)), 
        key=lambda x: x[1]
    )
    plt.figure(figsize=(10, 8))
    plt.xticks(list(range(47)), [k for k, _ in values])
    plt.bar(list(range(47)), [v for _, v in values])
    plt.rcParams['font.sans-serif'] = 'MS Gothic'
    plt.rcParams['axes.axisbelow'] = True
    plt.grid(axis='y')
    plt.margins(x=0.01)
    plt.savefig(bar_name, dpi=600, bbox_inches='tight')
    plt.close()
