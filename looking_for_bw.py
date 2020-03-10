import json
import os
import shutil

directory = r"C:\Users\Jeffrey\Desktop\ARC-master\kaggle_data_dump\evaluation"

#debugging only
colors_seen_count = dict()

# counts number of different colors in image
def colors_seen_in_image(image):
    colors_seen = set()
    for line in image:
        for pixel in line:
            colors_seen.add(pixel)
    return colors_seen

# going over all files, were each file represent one ARC question
for filename in os.listdir(directory):
    with open(directory+"\\"+filename, 'r') as f:
        data_dict = json.load(f)

    examples = data_dict['train']

    max_colors_seen = 0
    for example in examples:
        max_colors_seen = max(max_colors_seen,
                              len(colors_seen_in_image(example["input"])),
                              len(colors_seen_in_image(example["output"])))
    for example in data_dict['test']:
        max_colors_seen = max(max_colors_seen,
                              len(colors_seen_in_image(example["input"])),
                              len(colors_seen_in_image(example["output"])))
        
    if max_colors_seen in colors_seen_count:
        colors_seen_count[max_colors_seen] += 1
    else:
        colors_seen_count[max_colors_seen] = 1

    # copying all iq questions that have the potentital to be converted to black and white
    if max_colors_seen == 2:
        dst = r'C:\Users\Jeffrey\Desktop\ARC-master\eval_bw'
        shutil.copy(directory+"\\"+filename, dst)
