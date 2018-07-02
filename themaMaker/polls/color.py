from __future__ import print_function
import webcolors
import colorsys
import math


def convert_rgb_to_hls(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return (int(round(h * 360)) , int(round(l * 100)) , int(round(s * 100)) )

def convert_hex_to_rgb(value):
	#if type(value)==str:
	value = value.lstrip('#')
	lv = len(value)
	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
#print(convert_hex_to_rgb("#6789aa"))


def color_database():

	CSS_COLOR_NAMES = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","Darkorange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"];

	color_hex = [webcolors.name_to_hex(elem) for elem in CSS_COLOR_NAMES]

	color_rgb = [webcolors.name_to_rgb(elem) for elem in CSS_COLOR_NAMES]

	color_hls = [convert_rgb_to_hls(elem.red, elem.green, elem.blue) for elem in color_rgb]

	is_saturated_ar = [True if (elem[2] > 50 ) else False for elem in color_hls ]

	is_light_ar = [True if (elem[1] > 50 ) else False for elem in color_hls ]



	color_tendency_ar = ["Colorless" if (max(elem.red, elem.green, elem.blue) == elem.red == elem.green == elem.blue) else \
							("Red" if (max(elem.red, elem.green, elem.blue) == elem.red) else \
								("Green" if (max(elem.red, elem.green, elem.blue) == elem.green) else "Blue")) for elem in color_rgb ]

	color_list =[]


	for i in range(len(CSS_COLOR_NAMES)):
		color = {}
		color["color_id_hex"] = color_hex[i]
		color["color_name"] = CSS_COLOR_NAMES[i]
		color["is_light"] = is_light_ar[i]
		color["color_tendency"] = color_tendency_ar[i]
		color["is_saturated"] = is_saturated_ar[i]
		color_list.append(color)

	return color_list

def write_to_db():
	colors = color_database()
	for c in colors:
		col_hex = Color.objects.filter(color_id_hex=c["color_id_hex"])
		if col_hex.count()==0:
			c_new = Color(**c)
			c_new.save()
#write_to_db()


def color_tendency(color_id_hex):
	elem = convert_hex_to_rgb(color_id_hex)
	#elem = (red= color_rgb[0],green= color_rgb[1],blue= color_rgb[2])
	max_t = max(elem[0], elem[1], elem[2])
	tend = "Colorless" if (max_t == elem[0] == elem[1] == elem[2]) else \
							("Red" if (max_t == elem[0]) else \
								("Green" if (max_t == elem[1]) else "Blue"))
	return tend

#print(color_tendency("#FF7A41"))
#print(color_tendency("#00FFFF"))


def color_is_light(color_id_hex):
	elem_rgb = convert_hex_to_rgb(color_id_hex)
	elem_hls = convert_rgb_to_hls(elem_rgb[0],elem_rgb[1],elem_rgb[2])
	return (True if (elem_hls[1] > 50 ) else False)

def color_is_saturated(color_id_hex):
	elem_rgb = convert_hex_to_rgb(color_id_hex)
	elem_hls = convert_rgb_to_hls(elem_rgb[0],elem_rgb[1],elem_rgb[2])
	return (True if (elem_hls[2] > 50 ) else False)


def cg_group_tendency(color_list_hex):

	color_rgb_list = [convert_hex_to_rgb(elem) for elem in color_list_hex]
	color_tend_list = [color_tendency(elem) for elem in color_list_hex]
	word_counter = {}
	for word in color_tend_list:
		if word in word_counter:
			word_counter[word] += 1
		else:
			word_counter[word] = 1

	color_tend = sorted(word_counter, key = word_counter.get, reverse = True)
	return color_tend[0]


def color_render(color_hex):
	#color_hex is a hex value of a color without "#"
	colors = color_database() # !!! Read from database FIX IT LATER
	rendered_color = {}
	min_diff = 0xFF
	for item in colors:
		diff_red = abs( int((item["color_id_hex"][1:3]),16)-int(color_hex[0:2],16) )
		diff_green = abs( int((item["color_id_hex"][3:5]),16)-int(color_hex[2:4],16) )
		diff_blue = abs( int((item["color_id_hex"][5:7]),16)-int(color_hex[4:6],16) )
		values= [diff_red, diff_green, diff_blue]
		average = float(sum(values)) / 3
		if average < min_diff and item["color_tendency"] == color_tendency("#"+color_hex) :
			rendered_color = item

	print(color_hex + " is rendered to "+ rendered_color["color_id_hex"])

#color_render("FF7A41")

#print(color_hex)
#print(color_rgb)
#print(color_hls)
#print(is_saturated_ar)
#print(is_dark_ar)
#print(color_tendency_ar)

#print(color_list)