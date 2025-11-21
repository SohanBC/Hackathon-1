from PIL import Image
import imagehash

def compute_icon_similarity(fake_icon_path, original_icon_path):
    fake_hash = imagehash.average_hash(Image.open(fake_icon_path))
    orig_hash = imagehash.average_hash(Image.open(original_icon_path))

    diff = fake_hash - orig_hash
    score = 1 - (diff / 64)  # normalize
    return round(score, 2)
