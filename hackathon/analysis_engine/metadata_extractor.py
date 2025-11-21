def extract_metadata_score(fake_dev, real_dev):
    return 1 if fake_dev.lower() == real_dev.lower() else 0
