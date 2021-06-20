from matplotlib import pyplot as plt
from data import *


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
    plt.ylim(0, 65)
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

    sun = host.twinx()
    beautify_axis(sun, 1)
    sun.set_ylabel("Sun Spectrum [W/nm/m^2]")
    sun.yaxis.label.set_color("red")
    sun.set_ylim(0, 1.5)
    sun, = sun.plot(solar_spectrum.x, solar_spectrum.y, color="red", label="Solar Spectrum")

    sun_converted = host.twinx()
    beautify_axis(sun_converted, 1.1)
    sun_converted.set_ylabel("Sun Spectrum Converted [A/nm/m^2]")
    sun_converted.yaxis.label.set_color("green")
    sun_converted.set_ylim(0, 1.1)
    sun_converted, = sun_converted.plot(solar_spectrum_converted.x, solar_spectrum_converted.y, color="green",
                                        label="Solar Spectrum Converted")

    current = host.twinx()
    beautify_axis(current, 1.2)
    current.set_ylabel("Bottom Cell Current [mA/nm/cm^2]")
    current.yaxis.label.set_color("blue")
    current.set_ylim(0, 0.35)
    current, = current.plot(bottom_cell_current.x, bottom_cell_current.y, color="blue", label="Bottom Cell Current")

    lines = [sun, sun_converted, current]
    plt.legend(lines, [line.get_label() for line in lines], framealpha=0.85)
    fig.tight_layout()
    plt.show()
    plt.close("all")


def plot_currents():
    """plot the current distribution of the cells over wavelength"""
    plt.xlim(280, 900)
    plt.plot(*bottom_cell_current.plot_data, label="Bottom Cell")
    plt.plot(*bottom_cell_filtered_current.plot_data, label="Bottom Cell (filtered)")
    plt.plot(*top_cell_current.plot_data, label="Top Cell")
    plt.legend()

    plt.show()
    plt.close("all")


def plot_thickness_adjusted_current():
    """plot the current distribution of the cells over wavelength"""
    plt.xlim(280, 900)
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

    plt.ylim(-15, 5)
    plt.title("JV-Curves")
    plt.plot(*jv_bottom_cell.plot_data, label="Bottom Cell")
    plt.plot(*jv_bottom_cell_filtered.plot_data, label="Bottom Cell (filtered)")
    plt.plot(*jv_top_cell.plot_data, label="Top Cell")
    plt.legend()

    plt.show()
    plt.close("all")


def plot_jv_combined():
    fig, ax = plt.subplots()
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    plt.ylim(-15, 5)
    plt.title("JV-Curves combined")
    plt.plot(*jv_combined.plot_data, label="Combined")
    plt.plot(*jv_bottom_cell_filtered.plot_data, label="Bottom Cell (filtered)")
    plt.plot(*jv_top_cell.plot_data, label="Top Cell")
    plt.legend()

    plt.show()
    plt.close("all")


if __name__ == '__main__':
    # plot_eqe()
    # plot_solar_spectrum()
    # plot_currents()
    # plot_thickness_adjusted_current()
    plot_jv_separate()
    plot_jv_combined()
