from matplotlib import pyplot as plt
from main import *

plt.rcParams['figure.figsize'] = [12.0, 6.75]
plt.rcParams['figure.dpi'] = 200

show_figure = False

alpha = {"framealpha": 0.85}
dotted = {"linewidth": 2.5, "linestyle": "dotted"}
solid = {"linewidth": 2.5, "linestyle": "solid"}
color_bottom_cell = {"color": "red"}  # "#a02020"
color_bottom_cell_filtered = {"color": "limegreen"}
color_top_cell = {"color": "blue"}  # "#0020a0"
color_combined = {"color": "black"}  # "#010101"


def show_or_save(filename):
    if show_figure:
        plt.show()
    else:
        plt.savefig(filename, bbox_inches='tight')
    plt.close("all")


def beautify_axis(ax, shift):
    ax.spines["right"].set_position(("axes", shift))
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.spines["right"].set_visible(True)


def plot_eqe():
    """Plot the EQE Spectra"""
    plt.xlim(280, 900)
    plt.ylim(0, 0.65)
    plt.title("EQE Spectra")
    plt.xlabel(r"Wavelength [$nm$]")
    plt.ylabel(r"EQE [%]")
    plt.plot(eqe_bottom_cell.x, eqe_bottom_cell.y, label="EQE Bottom Cell", **color_bottom_cell_filtered, **dotted)
    plt.plot(eqe_bottom_cell_filtered.x, eqe_bottom_cell_filtered.y, label="EQE Bottom Cell (filtered)", **color_bottom_cell, **dotted)
    plt.plot(eqe_top_cell.x, eqe_top_cell.y, label="EQE Top Cell", **color_top_cell, **dotted)
    plt.legend(**alpha)

    show_or_save("plot_eqe.png")


def plot_solar_spectrum():
    plt.xlim(280, 900)
    plt.ylim(0, 1.75)
    plt.title("Given Solar Spectrum")
    plt.xlabel(r"Wavelength [$nm$]")
    plt.ylabel(r"Incident Power [$\frac{W}{nm \cdot m^2}$]")
    plt.plot(solar_spectrum.x, solar_spectrum.y, **solid)

    show_or_save("plot_solar_spectrum.png")


def plot_solar_spectra():
    """Plot the solar spectrum"""

    fig, host = plt.subplots()
    host.set_xlim(280, 900)
    plt.title("Solar Spectrum and Resulting Current")
    plt.xlabel(r"Wavelength [$nm$]")

    sun = host.twinx()
    beautify_axis(sun, 1)
    sun.set_ylabel(r"Sun Spectrum [$\frac{W}{nm \cdot m^2}$]")
    sun.yaxis.label.set_color("red")
    sun.set_ylim(0, 1.75)
    sun, = sun.plot(solar_spectrum.x, solar_spectrum.y, label="Solar Spectrum", **color_bottom_cell, **solid)

    sun_converted = host.twinx()
    beautify_axis(sun_converted, 1.1)
    sun_converted.set_ylabel(r"Sun Spectrum Converted [$\frac{A}{nm \cdot m^2}$]")
    sun_converted.yaxis.label.set_color("green")
    sun_converted.set_ylim(0, 1.3)
    sun_converted, = sun_converted.plot(solar_spectrum_converted.x, solar_spectrum_converted.y, label="Solar Spectrum Converted", **color_bottom_cell_filtered, **solid)

    current = host.twinx()
    beautify_axis(current, 1.2)
    current.set_ylabel(r"Bottom Cell Current [$\frac{mA}{nm \cdot cm^2}$]")
    current.yaxis.label.set_color("blue")
    current.set_ylim(0, 0.04)
    current, = current.plot(bottom_cell_current.x, bottom_cell_current.y, label="Bottom Cell Current", **color_top_cell, **solid)

    lines = [sun, sun_converted, current]
    plt.legend(lines, [line.get_label() for line in lines], framealpha=0.85)
    fig.tight_layout()
    show_or_save("plot_solar_spectra.png")


def plot_currents():
    """plot the current distribution of the cells over wavelength"""
    plt.xlim(280, 900)
    plt.ylim(0, 0.045)
    plt.title("Current Spectra")
    plt.xlabel(r"Wavelength [$nm$]")
    plt.ylabel(r"Current [$\frac{mA}{nm \cdot cm^2}$]")
    plt.plot(*bottom_cell_current.plot_data, label="Bottom Cell", **color_bottom_cell_filtered, **dotted)
    plt.plot(*bottom_cell_filtered_current.plot_data, label="Bottom Cell (filtered)", **color_bottom_cell, **dotted)
    plt.plot(*bottom_cell_current_scaled.plot_data, label="Bottom Cell (filtered, corrected)", **color_bottom_cell, **solid)
    plt.plot(*top_cell_current.plot_data, label="Top Cell", **color_top_cell, **dotted)
    plt.plot(*top_cell_current_scaled.plot_data, label="Top Cell (corrected)", **color_top_cell, **solid)
    plt.legend(**alpha)

    show_or_save("plot_currents.png")


def plot_thickness_adjusted_current():
    """plot the current distribution of the cells over wavelength"""
    plt.xlim(280, 900)
    plt.ylim(0, 0.02)
    plt.title("Current Spectra of Adjusted Cells")
    plt.xlabel(r"Wavelength [$nm$]")
    plt.ylabel(r"Current [$\frac{mA}{nm \cdot cm^2}$]")
    plt.plot(*bottom_cell_current_scaled.plot_data, label="Bottom Cell (filtered, corrected)", **color_bottom_cell, **solid)
    plt.plot(*top_cell_current_scaled.plot_data, label="Top Cell (corrected)", **color_top_cell, **solid)
    plt.legend(**alpha)

    show_or_save("plot_currents_adjusted.png")


def plot_jv_given():
    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.title("Given JV-Curves")
    plt.xlabel(r"Voltage [$V$]")
    plt.ylabel(r"Current [$\frac{mA}{cm^2}$]")

    plt.ylim(-15, 5)
    plt.plot(*jv_bottom_cell.plot_data, label="Bottom Cell", **color_bottom_cell_filtered, **dotted)
    plt.plot(*jv_bottom_cell_filtered.plot_data, label="Bottom Cell (filtered)", **color_bottom_cell, **dotted)
    plt.plot(*jv_top_cell.plot_data, label="Top Cell", **color_top_cell, **dotted)
    plt.legend(**alpha)

    show_or_save("plot_jv_given.png")


def plot_jv_separate():
    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.title("JV-Curves, Given and Adjusted")
    plt.xlabel(r"Voltage [$V$]")
    plt.ylabel(r"Current [$\frac{mA}{cm^2}$]")

    plt.ylim(-15, 5)
    plt.plot(*jv_bottom_cell.plot_data, label="Bottom Cell", **color_bottom_cell_filtered, **dotted)
    plt.plot(*jv_bottom_cell_filtered.plot_data, label="Bottom Cell (filtered)", **color_bottom_cell, **dotted)
    plt.plot(*jv_bottom_cell_corrected.plot_data, label="Bottom Cell (filtered, corrected)", **color_bottom_cell, **solid)
    plt.plot(*jv_top_cell.plot_data, label="Top Cell", **color_top_cell, **dotted)
    plt.plot(*jv_top_cell_corrected.plot_data, label="Top Cell (corrected)", **color_top_cell, **solid)
    plt.legend(**alpha)

    show_or_save("plot_jv.png")


def plot_jv_combined():
    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.title("JV-Curves of Integrated Cells")
    plt.xlabel(r"Voltage [$V$]")
    plt.ylabel(r"Current [$\frac{mA}{cm^2}$]")

    plt.ylim(-15, 5)
    plt.plot(*jv_combined.plot_data, label="Combined", **color_combined, **dotted)
    plt.plot(*jv_combined_corrected.plot_data, label="Combined (corrected)", **color_combined, **solid)
    plt.plot(*jv_bottom_cell_filtered.plot_data, label="Bottom Cell (filtered)", **color_bottom_cell, **dotted)
    plt.plot(*jv_bottom_cell_corrected.plot_data, label="Bottom Cell (filtered, corrected)", **color_bottom_cell, **solid)
    plt.plot(*jv_top_cell.plot_data, label="Top Cell", **color_top_cell, **dotted)
    plt.plot(*jv_top_cell_corrected.plot_data, label="Top Cell (corrected)", **color_top_cell, **solid)
    plt.legend(**alpha)

    show_or_save("plot_jv_combined.png")


def plot_jv_power():
    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.title("JV- and Power-Curves of Tandem Cells")
    ax.set_xlabel(r"Voltage [$V$]")
    ax.set_ylabel(r"Current [$\frac{mA}{cm^2}$]")
    ax.set_xlim(-0.5, 1.6)

    power = ax.twinx()
    power.set_ylabel(r"Power [$\frac{mW}{cm^2}$]")
    power.set_ylim(-5, 3)
    a, = power.plot(*power_combined.plot_data, **dotted, **color_bottom_cell, label="Combined Power")
    b, = power.plot(*power_combined_corrected.plot_data, **solid, **color_bottom_cell, label="Combined Power (corrected)")

    ax.set_ylim(-5, 3)
    c, = ax.plot(*jv_combined.plot_data, **dotted, label="Combined JV", **color_combined)
    d, = ax.plot(*jv_combined_corrected.plot_data, **solid, label="Combined JV (corrected)", **color_combined)

    lines = [a, b, c, d]
    plt.legend(lines, [line.get_label() for line in lines], framealpha=0.85, loc="upper center")
    fig.tight_layout()

    show_or_save("plot_power.png")


if __name__ == '__main__':
    plot_eqe()
    plot_solar_spectrum()
    plot_solar_spectra()
    plot_currents()
    plot_thickness_adjusted_current()
    plot_jv_given()
    plot_jv_separate()
    plot_jv_combined()
    plot_jv_power()
