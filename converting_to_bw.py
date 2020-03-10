import json
import os
import shutil

directory = r"C:\Users\Jeffrey\Desktop\ARC-master\eval_bw"

def colors_seen_in_image(image):
    colors_seen = set()
    for line in image:
        for pixel in line:
            colors_seen.add(pixel)
    return colors_seen

converted = 0
maxsize = []

# Converting all iq questions that can be converted to black and white to black and white.
for filename in os.listdir(directory):
    with open(directory+"\\"+filename, 'r+') as f:
        data = json.load(f)

        examples = data['train']
        question = data['test']
        color_sets_inputs = []
        color_sets_outputs = []
        for example in examples:
            color_sets_inputs.append(colors_seen_in_image(example['input']))
            color_sets_outputs.append(colors_seen_in_image(example['output']))
        for example in question:
            color_sets_inputs.append(colors_seen_in_image(example['input']))
            color_sets_outputs.append(colors_seen_in_image(example['output']))
        
        intersection_inputs = set.intersection(*color_sets_inputs)
        intersection_outputs = set.intersection(*color_sets_outputs)
        intersection = set.intersection(intersection_inputs,intersection_outputs)

        #if intersection contains 1 color, change it to black. The other color to white.
        #if intersection contains 2 colors, convert the first color to black and the second to white        
        
        if len(intersection) >= 1:
            size = 0
            
            color_to_black = list(intersection)[0]
            data['examples_size'] = []
            data['question_size'] = []
            for example in examples:
                size = max(size,len(example['input']),len(example['output']),len(example['input'][0]),
                              len(example['output'][0]))
                for i in range(len(example['input'])):
                    example['input'][i] = [0 if x == color_to_black else 1 for x in example['input'][i]]
                t = [len(example['input']),len(example['input'][0])]
                data['examples_size'].append(tuple(t))
                for i in range(len(example['output'])):
                    example['output'][i] = [0 if x == color_to_black else 1 for x in example['output'][i]]
                data['examples_size'].append(tuple([len(example['output']),len(example['output'][0])]))
            for example in question:
                size = max(size,len(example['input']),len(example['output']),len(example['input'][0]),
                              len(example['output'][0]))
                for i in range(len(example['input'])):
                    example['input'][i] = [0 if x == color_to_black else 1 for x in example['input'][i]]
                data['question_size'].append(tuple([len(example['input']),len(example['input'][0])]))
                for i in range(len(example['output'])):
                    example['output'][i] = [0 if x == color_to_black else 1 for x in example['output'][i]]
                data['question_size'].append(tuple([len(example['output']),len(example['output'][0])]))

            if size <= 19:
                converted+=1
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                
                dst = r'C:\Users\Jeffrey\Desktop\ARC-master\eval_bw_easy'
                shutil.copy(directory+"\\"+filename, dst)

            print(filename)
            
print("converted:",converted)
