from data import *

"""calculate the current of each cell"""
cell_size = 0.1e-4  # m^2 to 0.1cm^2
square_meter_to_square_centimeter = 1e-4
ampere_to_milli_ampere = 1000  # to convert from Ampere to milli ampere
to_percent = 0.01

# solar_spectrum = Data2D(*read_csv("sun_spectrum_direct_circumsolar.csv"))
solar_spectrum = Data2D(*read_csv("sun_spectrum_global_tilt.csv"))
solar_spectrum_converted = solar_energy_to_photon_count_to_charge(solar_spectrum)

eqe_bottom_cell = Data2D(*read_csv("eqe-kp115idtbr.csv")) * to_percent
bottom_cell_current = multiply_eqe_to_solar_spectrum(eqe_bottom_cell, solar_spectrum_converted) * square_meter_to_square_centimeter * ampere_to_milli_ampere
bottom_cell_current_integrated = bottom_cell_current.integrate()
print(f"{bottom_cell_current_integrated=}")

eqe_bottom_cell_filtered = Data2D(*read_csv("eqe-kp115idtbr-filtered.csv")) * to_percent
bottom_cell_filtered_current = multiply_eqe_to_solar_spectrum(eqe_bottom_cell_filtered, solar_spectrum_converted) * square_meter_to_square_centimeter * ampere_to_milli_ampere
bottom_cell_filtered_current_integrated = bottom_cell_filtered_current.integrate()
print(f"{bottom_cell_filtered_current_integrated=}")

eqe_top_cell = Data2D(*read_csv("eqe-p3htpcbm.csv")) * to_percent
top_cell_current = multiply_eqe_to_solar_spectrum(eqe_top_cell, solar_spectrum_converted) * square_meter_to_square_centimeter * ampere_to_milli_ampere
top_cell_current_integrated = top_cell_current.integrate()
print(f"{top_cell_current_integrated=}")

"""calculate the correction factor needed to match currents"""
# we were given the following to calculate the thickness correction factor for the top cell:
# P3HT*x = KP115filtered + (KP115-KP115filtered)*(1-x)
# => P*x = Kf + (K - Kf) * (1-x)
# => x = K / (P + K + Kf)
correction_factor = bottom_cell_current_integrated / (top_cell_current_integrated + bottom_cell_current_integrated - bottom_cell_filtered_current_integrated)
print(f"{correction_factor=}")

top_cell_current_scaled = top_cell_current * correction_factor
print(f"{top_cell_current_scaled.integrate()=}")
bottom_cell_current_scaled = bottom_cell_filtered_current + (bottom_cell_current - bottom_cell_filtered_current) * (1 - correction_factor)
print(f"{bottom_cell_current_scaled.integrate()=}")

"""get and sum JV curves"""
jv_top_cell = Data2D(*read_csv("jv-p3htpcbm.csv"))
jv_top_cell_corrected = jv_top_cell * correction_factor
jv_bottom_cell = Data2D(*read_csv("jv-kp115idtbr.csv"))
jv_bottom_cell_filtered = Data2D(*read_csv("jv-kp115idtbr-filtered.csv"))
jv_bottom_cell_corrected = jv_bottom_cell_filtered + (jv_bottom_cell - jv_bottom_cell_filtered) * (1 - correction_factor)
jv_combined = combine_jv_curves(jv_bottom_cell_filtered, jv_top_cell)
jv_combined_corrected = combine_jv_curves(jv_bottom_cell_corrected, jv_top_cell_corrected)
power_combined = jv_to_power(jv_combined)
power_combined_corrected = jv_to_power(jv_combined_corrected)
print(f"{power_combined.peak_y()=} mW/cm²")
print(f"{power_combined_corrected.peak_y()=} mW/cm²")
