from bokeh.layouts import layout
from bokeh.models import Div, RangeSlider, Spinner
from bokeh.plotting import figure, show

from main import *

"""
fig, ax = plt.subplots()
ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
plt.xlabel(r"Voltage [$V$]")
plt.ylabel(r"Current [$\frac{mA}{cm^2}$]")

plt.ylim(-15, 5)
plt.title("JV-Curves combined")
plt.plot(*jv_combined.plot_data, **args, label="Combined", color="#010101")
plt.plot(*jv_combined_corrected.plot_data, **args_corrected, label="Combined (corrected)", color="#010101")
plt.plot(*jv_bottom_cell_filtered.plot_data, **args, label="Bottom Cell (filtered)", color="#a02020")
plt.plot(*jv_bottom_cell_corrected.plot_data, **args_corrected, label="Bottom Cell (filtered, corrected)", color="#a02020")
plt.plot(*jv_top_cell.plot_data, **args, label="Top Cell", color="#0020a0")
plt.plot(*jv_top_cell_corrected.plot_data, **args_corrected, label="Top Cell (corrected)", color="#0020a0")
plt.legend()

plt.show()
plt.close("all")
"""


# prepare some data
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [4, 5, 5, 7, 2, 6, 4, 9, 1, 3]

# create plot with circle glyphs
p = figure(y_range=(-15, 5), x_range=(-1, 1), plot_width=500, plot_height=250)
a = p.line(x=jv_combined.x, y=jv_combined.y, legend_label="Combined")
b = p.line(x=jv_combined_corrected.x, y=jv_combined_corrected.y, legend_label="Combined (corrected)")
c = p.line(x=jv_bottom_cell_filtered.x, y=jv_bottom_cell_filtered.y, legend_label="Bottom Cell")
d = p.line(x=jv_bottom_cell_corrected.x, y=jv_bottom_cell_corrected.y, legend_label="Bottom Cell (filtered, corrected)")
e = p.line(x=jv_top_cell.x, y=jv_top_cell.y, legend_label="Top Cell")
f = p.line(x=jv_top_cell_corrected.x, y=jv_top_cell_corrected.y, legend_label="Top Cell (corrected)")

# set up textarea (div)
#div = Div(
#    text="""
#          <p>Select the circle's size using this control element:</p>
#          """,
#    width=200,
#    height=30,
#)

# set up spinner
#spinner = Spinner(
#    title="Circle size",
#    low=0,
#    high=60,
#    step=5,
#    value=points.glyph.size,
#    width=200,
#)
#spinner.js_link("value", points.glyph, "size")

# set up RangeSlider
range_slider = RangeSlider(
    title="Adjust x-axis range",
    start=0,
    end=10,
    step=1,
    value=(p.x_range.start, p.x_range.end),
)
range_slider.js_link("value", p.x_range, "start", attr_selector=0)
range_slider.js_link("value", p.x_range, "end", attr_selector=1)

# create layout
layout = layout(
    [
        [range_slider],
        [p],
    ]
)

# show result
show(layout)
