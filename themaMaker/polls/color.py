from __future__ import print_function
import webcolors
import colorsys



def convert_rgb_to_hls(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return (int(round(h * 360)) , int(round(l * 100)) , int(round(s * 100)) )


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



#print(color_hex)
#print(color_rgb)
#print(color_hls)
#print(is_saturated_ar)
#print(is_dark_ar)
#print(color_tendency_ar)

#print(color_list)