def print_debug(captions):
    print()
    for caption in captions:
        print(f"strip: {caption.sound_strip}")
        print(f"frame_start: {caption.sound_strip.frame_start}")