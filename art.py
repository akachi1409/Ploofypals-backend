from PIL import Image 
from IPython.display import display 
import random
import json
import os

dirs = [
    "Armor",
    "Eyes",
    "Hands",
    "Head",
    "Helmet",
    "Mouth",
    "Panel",
    "Weapon",
    "Feet"
]

TOTAL_IMAGES = 50
all_images = [] 

eyes = []
eyes_weights = []
eyes_files = {}

head = []
head_weights = []
head_files = {}

armor = []
armor_weights=[]
armor_files = {}

helmet = []
helmet_weights = []
helmet_files = {}

mouth = []
mouth_weights = []
mouth_files = {}

hands = []
hands_weights = []
hands_files = {}

weapon = []
weapon_weights = []
weapon_files = {}

feet = []
feet_weights = []
feet_files = {}

panel = []
panel_weights = []
panel_files = {}

def handle_data (item, item_weight, item_files, data):
    index = 0;
    names = data['names']
    raritys = data['rarity']
    
    for name in names.split(","):
        item.append(data['trait']+"_"+ str(index))
        item_files.setdefault(item[index], name.split(".")[0])
        index = index + 1
    for rarity in raritys.split(","):
        item_weight.append( int(rarity) )
        
    
def read_json_data ( data ):
    print("data:", data)
    trait = data['trait']
    if trait == "Eyes":
        handle_data( eyes, eyes_weights, eyes_files, data);
    if trait == "Head":
        handle_data( head, head_weights, head_files, data)
    if trait == "Armor":
        handle_data( armor, armor_weights, armor_files, data)
    if trait == "Helmet":
        handle_data( helmet, helmet_weights, helmet_files, data)
    if trait == "Mouth":
        handle_data(mouth, mouth_weights, mouth_files, data)
    if trait == "Hands":
        handle_data(hands, hands_weights, hands_files, data)
    if trait == "Weapon":
        handle_data(weapon, weapon_weights, weapon_files, data)
    if trait == "Feet":
        handle_data(feet, feet_weights, feet_files, data)
    if trait == "Panel":
        handle_data(panel, panel_weights, panel_files, data)

def create_new_image():
    
    new_image = {} #
   
    new_image ["armor"] = random.choices(armor, armor_weights)[0]
    #new_image ["bg"] = random.choices(bg, bg_weights)[0]
    #new_image ["breed"] = random.choices(breed, breed_weights)[0]
    new_image ["eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image ["feet"] = random.choices(feet, feet_weights)[0]
    new_image ["hands"] = random.choices(hands, hands_weights)[0]
    new_image ["head"] = random.choices(head, head_weights)[0]
    new_image ["helmet"] = random.choices(helmet, helmet_weights)[0]
    new_image ["mouth"] = random.choices(mouth, mouth_weights)[0]
    new_image ["panel"] = random.choices(panel, panel_weights)[0]
    new_image ["weapon"] = random.choices(weapon, weapon_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image           
    
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("dirs:", dirs);
for directory in dirs:
    with open("./uploads/" + directory+ "/data.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        read_json_data(jsonObject)
        jsonFile.close()

print("JSON data is processed!")


print("Creating new images are started.")
for i in range(TOTAL_IMAGES): 
    
    new_trait_image = create_new_image()
    
    all_images.append(new_trait_image)

print("Are all images unique?", all_images_unique(all_images))

i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1
   
armor_count = {}
for item in armor:
    armor_count[item] = 0
    
eyes_count = {}
for item in eyes:
    eyes_count[item] = 0;

head_count = {}
for item in head:
    head_count[item] = 0    

helmet_count = {}
for item in helmet:
    helmet_count[item] = 0
    
mouth_count = {}
for item in mouth:
    mouth_count[item] = 0
    
hands_count = {}
for item in hands:
    hands_count[item] = 0;
    
weapon_count = {}
for item in weapon:
    weapon_count[item] = 0
    
feet_count = {}
for item in feet:
    feet_count[item] = 0

panel_count = {}
for item in panel:
    panel_count[item] = 0
    
for image in all_images:
    armor_count[image["armor"]] += 1
    eyes_count[image["eyes"]] += 1
    feet_count[image["feet"]] += 1
    hands_count[image["hands"]] += 1
    head_count[image["head"]] += 1
    helmet_count[image["helmet"]] += 1
    mouth_count[image["mouth"]] += 1
    feet_count[image["feet"]] += 1
    weapon_count[image["weapon"]] += 1
    panel_count[image["panel"]] += 1

for item in all_images:

    im1 = Image.open(f'./uploads/Head/{head_files[item["head"]]}.png').convert('RGBA')
    im2 = Image.open(f'./uploads/Eyes/{eyes_files[item["eyes"]]}.png').convert('RGBA')
    im3 = Image.open(f'./uploads/Armor/{armor_files[item["armor"]]}.png').convert('RGBA')
    im4 = Image.open(f'./uploads/Helmet/{helmet_files[item["helmet"]]}.png').convert('RGBA')
    im5 = Image.open(f'./uploads/Mouth/{mouth_files[item["mouth"]]}.png').convert('RGBA')
    im6 = Image.open(f'./uploads/Hands/{hands_files[item["hands"]]}.png').convert('RGBA')
    im7 = Image.open(f'./uploads/Weapon/{weapon_files[item["weapon"]]}.png').convert('RGBA')
    im8 = Image.open(f'./uploads/Feet/{feet_files[item["feet"]]}.png').convert('RGBA')
    im9 = Image.open(f'./uploads/Panel/{panel_files[item["panel"]]}.png').convert('RGBA')
    
    #com10 = Image.alpha_composite(com9, im10)
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)
    com6 = Image.alpha_composite(com5, im7)
    com7 = Image.alpha_composite(com6, im9)
    com8 = Image.alpha_composite(com7, im8)
    
    rgb_im = com8.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./result/" + file_name)
'''    


feet = ['blue', 'pink', 'purple']
feet_weights = [33, 33, 33]

hands = ['blue', 'pink', 'purple']
hands_weights = [33, 33, 33]

mouth = ['circle', 'diamond', 'square']
mouth_weights = [33, 33, 33]

panel = ['aqua', 'grey', 'salmon']
panel_weights = [33, 33, 33]

weapon = ['spear', 'split', 'sword']
weapon_weights = [33, 33, 33]



feet_files = {
    'blue': 'Blue (Common)', 
    'pink': 'Pink (Common)', 
    'purple': 'Purple (Uncommon)', 
}
hands_files={
    'blue':'Blue (Common)',
    'pink':'Pink (Common)',
    'purple':'Purple (Uncommon)'
}

mouth_files = {
    'circle': 'Circle (Common)', 
    'diamond': 'Diamond (Uncommon)', 
    'square': 'Square (Common)', 
}
panel_files = {
    'aqua':'Aqua Marine (Common)',
    'grey':'Grey (Common)',
    'salmon':'Salmon (Uncommon)'    
}
weapon_files = {
    'spear': 'Spear (Common)', 
    'split': 'Split Sword (Uncommon)', 
    'sword': 'Sword (Common)', 
}



feet_count = {}
for item in feet:
    feet_count[item] = 0
    
hands_count = {}
for item in hands:
    hands_count[item] = 0
    
helmet_count = {}
for item in helmet:
    helmet_count[item] = 0
    
mouth_count = {}
for item in mouth:
    mouth_count[item] = 0

panel_count = {}
for item in panel:
    panel_count[item] = 0
    
weapon_count = {}
for item in weapon:
    weapon_count[item] = 0


    '''