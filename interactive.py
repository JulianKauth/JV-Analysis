from bokeh.layouts import layout
from bokeh.models import Div, RangeSlider, Spinner, CheckboxGroup, Toggle
from bokeh.plotting import figure, show

from main import *
# tutorial_ https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_9.html
# docs: https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

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

# create plot with circle glyphs
p = figure(plot_width=1000, plot_height=600, sizing_mode="stretch_both")
a = p.line(x=jv_combined.x, y=jv_combined.y, legend_label="Combined")
b = p.line(x=jv_combined_corrected.x, y=jv_combined_corrected.y, legend_label="Combined (corrected)")
c = p.line(x=jv_bottom_cell_filtered.x, y=jv_bottom_cell_filtered.y, legend_label="Bottom Cell")
d = p.line(x=jv_bottom_cell_corrected.x, y=jv_bottom_cell_corrected.y, legend_label="Bottom Cell (filtered, corrected)")
e = p.line(x=jv_top_cell.x, y=jv_top_cell.y, legend_label="Top Cell")
f = p.line(x=jv_top_cell_corrected.x, y=jv_top_cell_corrected.y, legend_label="Top Cell (corrected)")

# set up RangeSlider
#range_slider = RangeSlider(
#    title="Adjust x-axis range",
#    start=0,
#    end=10,
#    step=1,
#    value=(p.x_range.start, p.x_range.end),
#)
#range_slider.js_link("value", p.x_range, "start", attr_selector=0)
#range_slider.js_link("value", p.x_range, "end", attr_selector=1)

toggle_a = Toggle(label="a", active=True)
toggle_a.js_link("active", a, "visible")
toggle_b = Toggle(label="b", active=True)
toggle_b.js_link("active", b, "visible")
toggle_c = Toggle(label="c", active=True)
toggle_c.js_link("active", c, "visible")
toggle_d = Toggle(label="d", active=True)
toggle_d.js_link("active", d, "visible")
toggle_e = Toggle(label="e", active=True)
toggle_e.js_link("active", e, "visible")
toggle_f = Toggle(label="f", active=True)
toggle_f.js_link("active", f, "visible")

# create layout
layout = layout(
    [
        [toggle_a, p],
        [toggle_b],
        [toggle_c],
        [toggle_d],
        [toggle_e],
        [toggle_f]
    ]
)

# show result
show(layout)

