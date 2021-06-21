from matplotlib import pyplot as plt
from main import *

args = {"linewidth": 2.5, "linestyle": "dotted"}
args_corrected = {"linewidth": 2.5, "linestyle": "solid"}


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
    plt.xlabel(r"Wavelength [$nm$]")
    plt.ylabel(r"EQE [%]")
    plt.plot(eqe_bottom_cell.x, eqe_bottom_cell.y, label="EQE Bottom Cell")
    plt.plot(eqe_bottom_cell_filtered.x, eqe_bottom_cell_filtered.y, label="EQE Bottom Cell (filtered)")
    plt.plot(eqe_top_cell.x, eqe_top_cell.y, label="EQE Top Cell")
    plt.legend()

    plt.show()
    plt.close("all")


def plot_solar_spectrum():
    """Plot the solar spectrum"""

    fig, host = plt.subplots()
    host.set_xlim(280, 900)
    plt.xlabel(r"Wavelength [$nm$]")

    sun = host.twinx()
    beautify_axis(sun, 1)
    sun.set_ylabel(r"Sun Spectrum [$\frac{W}{nm \cdot m^2}$]")
    sun.yaxis.label.set_color("red")
    sun.set_ylim(0, 1.75)
    sun, = sun.plot(solar_spectrum.x, solar_spectrum.y, color="red", label="Solar Spectrum")

    sun_converted = host.twinx()
    beautify_axis(sun_converted, 1.1)
    sun_converted.set_ylabel(r"Sun Spectrum Converted [$\frac{A}{nm \cdot m^2}$]")
    sun_converted.yaxis.label.set_color("green")
    sun_converted.set_ylim(0, 1.3)
    sun_converted, = sun_converted.plot(solar_spectrum_converted.x, solar_spectrum_converted.y, color="green", label="Solar Spectrum Converted")

    current = host.twinx()
    beautify_axis(current, 1.2)
    current.set_ylabel(r"Bottom Cell Current [$\frac{mA}{nm \cdot cm^2}$]")
    current.yaxis.label.set_color("blue")
    current.set_ylim(0, 0.04)
    current, = current.plot(bottom_cell_current.x, bottom_cell_current.y, color="blue", label="Bottom Cell Current")

    lines = [sun, sun_converted, current]
    plt.legend(lines, [line.get_label() for line in lines], framealpha=0.85)
    fig.tight_layout()
    plt.show()
    plt.close("all")


def plot_currents():
    """plot the current distribution of the cells over wavelength"""
    plt.xlim(280, 900)
    plt.ylim(0, 0.045)
    plt.xlabel(r"Wavelength [$nm$]")
    plt.ylabel(r"Current [$\frac{mA}{nm \cdot cm^2}$]")
    plt.plot(*bottom_cell_current.plot_data, label="Bottom Cell")
    plt.plot(*bottom_cell_filtered_current.plot_data, label="Bottom Cell (filtered)")
    plt.plot(*bottom_cell_current_scaled.plot_data, label="Bottom Cell (filtered, corrected)")
    plt.plot(*top_cell_current.plot_data, label="Top Cell")
    plt.plot(*top_cell_current_scaled.plot_data, label="Top Cell (corrected)")
    plt.legend()

    plt.show()
    plt.close("all")


def plot_thickness_adjusted_current():
    """plot the current distribution of the cells over wavelength"""
    plt.xlim(280, 900)
    plt.ylim(0, 0.02)
    plt.xlabel(r"Wavelength [$nm$]")
    plt.ylabel(r"Current [$\frac{mA}{nm \cdot cm^2}$]")
    # plt.plot(*bottom_cell_current.plot_data, label="Bottom Cell")
    plt.plot(*bottom_cell_current_scaled.plot_data, label="Bottom Cell (filtered)")
    plt.plot(*top_cell_current_scaled.plot_data, label="Top Cell")
    plt.legend()

    plt.show()
    plt.close("all")


def plot_jv_separate():
    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.xlabel(r"Voltage [$V$]")
    plt.ylabel(r"Current [$\frac{mA}{cm^2}$]")

    plt.ylim(-15, 5)
    plt.title("JV-Curves")
    plt.plot(*jv_bottom_cell.plot_data, label="Bottom Cell")
    plt.plot(*jv_bottom_cell_filtered.plot_data, label="Bottom Cell (filtered)")
    plt.plot(*jv_bottom_cell_corrected.plot_data, label="Bottom Cell (filtered, corrected)")
    plt.plot(*jv_top_cell.plot_data, label="Top Cell")
    plt.plot(*jv_top_cell_corrected.plot_data, label="Top Cell (corrected)")
    plt.legend()

    plt.show()
    plt.close("all")


def plot_jv_combined():
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


def plot_jv_power():
    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.set_xlabel(r"Voltage [$V$]")
    ax.set_ylabel(r"Current [$\frac{mA}{cm^2}$]")
    ax.set_xlim(-0.5, 1.6)

    power = ax.twinx()
    power.set_ylabel(r"Power [$\frac{mW}{cm^2}$]")
    power.set_ylim(-5, 3)
    a, = power.plot(*power_combined.plot_data, **args, color="red", label="Combined Power")
    b, = power.plot(*power_combined_corrected.plot_data, **args_corrected, color="red", label="Combined Power (corrected)")

    ax.set_ylim(-5, 3)
    c, = ax.plot(*jv_combined.plot_data, **args, label="Combined JV", color="#010101")
    d, = ax.plot(*jv_combined_corrected.plot_data, **args_corrected, label="Combined JV (corrected)", color="#010101")

    lines = [a, b, c, d]
    plt.legend(lines, [line.get_label() for line in lines], framealpha=0.85, loc="upper center")
    fig.tight_layout()

    plt.show()
    plt.close("all")


if __name__ == '__main__':
    # plot_eqe()
    # plot_solar_spectrum()
    # plot_currents()
    # plot_thickness_adjusted_current()
    # plot_jv_separate()
    plot_jv_combined()
    plot_jv_power()
