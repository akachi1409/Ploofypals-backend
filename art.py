from PIL import Image, ImageSequence
from IPython.display import display 
import random
import json
import os
from zipfile import ZipFile

#fire_gif = Image.open(f'./uploads/Breed/Fire1.gif')
dirs = [
    "Background",
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

background = []
background_weights = []
background_files = {}
background_rarity = []

fires = []
fires_weights = []
fires_files = {}
fires_rarity = []

eyes = []
eyes_weights = []
eyes_files = {}
eyes_rarity = []

head = []
head_weights = []
head_files = {}
head_rarity = []

armor = []
armor_weights=[]
armor_files = {}
armor_rarity = []

helmet = []
helmet_weights = []
helmet_files = {}
helmet_rarity = []

mouth = []
mouth_weights = []
mouth_files = {}
mouth_rarity = []

hands = []
hands_weights = []
hands_files = {}
hands_rarity = []

weapon = []
weapon_weights = []
weapon_files = {}
weapon_rarity = []

feet = []
feet_weights = []
feet_files = {}
feet_rarity = []

panel = []
panel_weights = []
panel_files = {}
panel_rarity=[]

def handle_data (item, item_weight, item_files, item_rarity, data):
    index = 0;
    names = data['names']
    raritys = data['rarity']
    types = data['types'].split(",")
    for name in names.split(","):
        item.append(data['trait']+"_"+ str(index))
        item_files.setdefault(item[index], name.split(".")[0])
        item_rarity.append(types[index])
        index = index + 1
    for rarity in raritys.split(","):
        item_weight.append( int(rarity) )
        
    
def read_json_data ( data ):
    print("data:", data)
    trait = data['trait']
    if trait == "Background":
        handle_data(background, background_weights, background_files, background_rarity, data)
    if trait == "Eyes":
        handle_data( eyes, eyes_weights, eyes_files, eyes_rarity, data);
    if trait == "Head":
        handle_data( head, head_weights, head_files, head_rarity, data)
    if trait == "Armor":
        handle_data( armor, armor_weights, armor_files, armor_rarity, data)
    if trait == "Helmet":
        handle_data( helmet, helmet_weights, helmet_files, helmet_rarity, data)
    if trait == "Mouth":
        handle_data(mouth, mouth_weights, mouth_files, mouth_rarity, data)
    if trait == "Hands":
        handle_data(hands, hands_weights, hands_files, hands_rarity, data)
    if trait == "Weapon":
        handle_data(weapon, weapon_weights, weapon_files, weapon_rarity, data)
    if trait == "Feet":
        handle_data(feet, feet_weights, feet_files, feet_rarity, data)
    if trait == "Panel":
        handle_data(panel, panel_weights, panel_files, panel_rarity, data)
    if trait == "Breed":
        handle_data(fires, fires_weights, fires_files, fires_rarity, data)

def create_new_image():
    
    new_image = {} #
   
    new_image ["background"] = random.choices(background, background_weights)[0]
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
    new_image ["breed"] = random.choices(fires, fires_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image           
    
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

def make_zip(dir1):
    zipObj = ZipFile('./result/' + dir1 + '/result.zip', 'w')
    directory = "./result/"+ dir1
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if (os.path.isfile(f)):
            if (filename != "result.zip"):
                zipObj.write(f)
            #print(filename)
            #zipObj.write(f)
    zipObj.close()
    
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
   
background_count = {}
for item in background:
    background_count[item] = 0

fires_count = {}
for item in fires:
    fires_count[item] = 0
    
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
    background_count[image["background"]] += 1
    fires_count[image["breed"]] += 1
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



def check_rarity(index, item_rarity):
    index = int(index)
    type1 = item_rarity[index]
    if int(type1) == 1:
        return 0
    else :
        return 1
    
for item in all_images:
    common = 0
    im0 = Image.open(f'./uploads/Background/{background_files[item["background"]]}.png').convert('RGBA')
    background_index = item["background"].split("_")[1]
    fire_gif = Image.open(f'./uploads/Breed/{fires_files[item["breed"]]}.gif')
    #fire_index = item["fires"].split("_")[1]
    im1 = Image.open(f'./uploads/Head/{head_files[item["head"]]}.png').convert('RGBA')
    head_index = item["head"].split("_")[1]
    im2 = Image.open(f'./uploads/Eyes/{eyes_files[item["eyes"]]}.png').convert('RGBA')
    eyes_index = item["eyes"].split("_")[1]
    im3 = Image.open(f'./uploads/Armor/{armor_files[item["armor"]]}.png').convert('RGBA')
    armor_index = item["armor"].split("_")[1]
    im4 = Image.open(f'./uploads/Helmet/{helmet_files[item["helmet"]]}.png').convert('RGBA')
    helmet_index = item["helmet"].split("_")[1]
    im5 = Image.open(f'./uploads/Mouth/{mouth_files[item["mouth"]]}.png').convert('RGBA')
    mouth_index = item["mouth"].split("_")[1]
    im6 = Image.open(f'./uploads/Hands/{hands_files[item["hands"]]}.png').convert('RGBA')
    hands_index = item["hands"].split("_")[1]
    im7 = Image.open(f'./uploads/Weapon/{weapon_files[item["weapon"]]}.png').convert('RGBA')
    weapon_index = item["weapon"].split("_")[1]
    im8 = Image.open(f'./uploads/Feet/{feet_files[item["feet"]]}.png').convert('RGBA')
    feet_index = item["feet"].split("_")[1]
    im9 = Image.open(f'./uploads/Panel/{panel_files[item["panel"]]}.png').convert('RGBA')
    panel_index = item["panel"].split("_")[1]
    
    common += check_rarity(background_index, background_rarity)
    
    common += check_rarity(head_index, head_rarity)
    common += check_rarity(eyes_index, eyes_rarity)
    common += check_rarity(armor_index, armor_rarity)
    common += check_rarity(helmet_index, helmet_rarity)
    common += check_rarity(mouth_index, mouth_rarity)
    common += check_rarity(hands_index, hands_rarity)
    common += check_rarity(weapon_index, weapon_rarity)
    common += check_rarity(feet_index, feet_rarity)
    common += check_rarity(panel_index, panel_rarity)
    print("---", common)
  
    
    
    
    
    if common >=9 :
        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)
        com6 = Image.alpha_composite(com5, im7)
        com7 = Image.alpha_composite(com6, im9)
        com8 = Image.alpha_composite(com7, im8)
        file_name = str(item["tokenId"]) + ".gif"
        frames = []
        width, height = fire_gif.size
        for num in range(0, fire_gif.n_frames, 5):
            fire_gif.seek(num)
            layer = Image.new("RGBA", (width, height), (0, 0 , 0 , 0))
            layer.paste(fire_gif, (0, 0))
            layer.paste(com8, (0, 0) , mask = com8)
            frames.append(layer)
            frames[0].save("./result/legendary/" + file_name, 
                           save_all= True,
                           append_images = frames[1:],
                           loop = 0
                           )
    if common > 2 and common <9:
        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)
        com6 = Image.alpha_composite(com5, im7)
        com7 = Image.alpha_composite(com6, im9)
        com8 = Image.alpha_composite(com7, im8)
        file_name = str(item["tokenId"]) + ".gif"
        frames = []
        width, height = fire_gif.size
        for num in range(0, fire_gif.n_frames, 5):
            fire_gif.seek(num)
            layer = Image.new("RGBA", (width, height), (0, 0 , 0 , 0))
            layer.paste(fire_gif, (0, 0))
            layer.paste(com8, (0, 0) , mask = com8)
            frames.append(layer)
            frames[0].save("./result/rare/" + file_name, 
                           save_all= True,
                           append_images = frames[1:],
                           loop = 0
                           )
    if common <=2:
        com0 = Image.alpha_composite(im0, im1)
        com1 = Image.alpha_composite(com0, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)
        com6 = Image.alpha_composite(com5, im7)
        com7 = Image.alpha_composite(com6, im9)
        com8 = Image.alpha_composite(com7, im8)
        file_name = str(item["tokenId"]) + ".png"
        rgb_im = com8.convert('RGB')
        rgb_im.save("./result/normal/" + file_name)
    
    #rgb_im.save("./result/" + file_name)
    #com8.save("./result" + file_name)
    #"""frames = []
    
    """
    frames = []
    print("start gif processing------")
    for frame in ImageSequence.Iterator(fire_gif):
        output = im1.copy()
        frame_px = frame.load()
        output_px = output.load()
        transparent_foreground = frame.convert("RGBA")
        transparent_foreground_px = transparent_foreground.load()
        for x in range(frame.width):
            for y in range(frame.height):
                if frame_px[x,y] in (frame.info["background"], frame.info("transparency")):
                    continue
                output_px = transparent_foreground_px[x,y]
                #if frame_px[x, y] in ( frame.info)
        #frame = frame.copy()
        #frame.paste(im1, mask=im1)
        #frame = frame.convert("RGB")
        frames.append(output)
    print("end processing git----")
    frames[0].save("./result/" + file_name, save_all= True, append_images = frames[1:])
    """
make_zip("legendary")
make_zip("rare")
make_zip("normal")