# /// script
# dependencies = [
#     "fonttools",
# ]
# ///



from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen

# 1. Load the font file
font = TTFont("PlaywriteAR-Regular.ttf")  # Playwrite-Argentina
glyph_set = font.getGlyphSet()
glyph_name = font.getBestCmap()[ord("j")]

# 2. Calculate the exact bounding box of the glyph in font coordinates
bounds_pen = BoundsPen(glyph_set)
glyph_set[glyph_name].draw(bounds_pen)
xMin, yMin, xMax, yMax = bounds_pen.bounds
print(f"{bounds_pen.bounds=}")

# 3. Define padding and calculate dynamic viewBox for flipped Y-axis
padding = 60
vb_x = xMin - padding
vb_y = -yMax - padding
vb_width = (xMax - xMin) + (2 * padding)
vb_height = (yMax - yMin) + (2 * padding)

# 4. Extract path data with vertical flip transform
svg_pen = SVGPathPen(glyph_set)
transform_pen = TransformPen(svg_pen, Transform(1, 0, 0, -1, 0, 0))
glyph_set[glyph_name].draw(transform_pen)
path_data = svg_pen.getCommands()

# 5. Write out the standalone SVG file
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x} {vb_y} {vb_width} {vb_height}">
  <path d="{path_data}" />
</svg>'''

with open("playwrite-argentina-j.svg", "w") as f:
    f.write(svg_content)

print("Successfully generated playwrite-argentina-j.svg with all components included.")
