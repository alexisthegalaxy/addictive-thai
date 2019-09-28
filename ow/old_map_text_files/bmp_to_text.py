# from PIL import Image
#
# from overworld.overworld import CellTypes
#
#
# def convert_bmp_to_text(input_file: str, output_file: str = ""):
#     cell_type_names = [a for a in dir(CellTypes) if not a.startswith('__')]
#     if output_file == "":
#         output_file = input_file[:-4]
#     im = Image.open(input_file)  # Can be many different formats.
#     pix = im.load()
#
#     t = ""
#
#     width, height = im.size
#     for x in range(height):
#         for y in range(width):
#             color = pix[y, x]
#             color_found = False
#             for cell_type_name in cell_type_names:
#                 cell_type = getattr(CellTypes, cell_type_name)
#                 if color == cell_type.color:
#                     color_found = True
#                     t += cell_type.letter
#             if not color_found:
#                 t += CellTypes.none.letter
#         t += "\n"
#     t = t[:-1]
#     f = open(output_file, "w+")
#     f.write(t)
#     return t
#
#
# convert_bmp_to_text('wakaba.bmp')
# convert_bmp_to_text('house1.bmp')
# convert_bmp_to_text('house2.bmp')
# convert_bmp_to_text('house3.bmp')
# convert_bmp_to_text('labo.bmp')
# convert_bmp_to_text('road1.bmp')
# convert_bmp_to_text('road2.bmp')
# convert_bmp_to_text('road3.bmp')
# convert_bmp_to_text('road4.bmp')
# convert_bmp_to_text('kikyou.bmp')
# convert_bmp_to_text('tsunagari.bmp')
# convert_bmp_to_text('hiwada.bmp')
# convert_bmp_to_text('ubame.bmp')
# convert_bmp_to_text('kogane.bmp')
# convert_bmp_to_text('pass1.bmp')
# convert_bmp_to_text('pass2.bmp')
# convert_bmp_to_text('pass3.bmp')
# convert_bmp_to_text('inn1.bmp')
# convert_bmp_to_text('inn2.bmp')
# convert_bmp_to_text('inn_khonkaen.bmp')
# convert_bmp_to_text('inn_buengsamphan.bmp')
# convert_bmp_to_text('full_map.bmp')
