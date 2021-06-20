class Data2D:
    def __init__(self, x, y):
        self.x = list(x).copy()
        self.y = list(y).copy()

    @staticmethod
    def get_value_at(x, y, searched_x):
        # if we don't span this range, return 0
        if not x[0] <= searched_x <= x[-1]:
            return 0
        # if we have the element, return it
        if searched_x in x:
            return y[x.index(searched_x)]
        # now we do linear interpolation
        x0, x1, y0, y1 = (0, 0, 0, 0)
        for x, y in zip(x, y):
            if x > searched_x:
                x1, y1 = x, y
                break
            x0, y0 = x, y
        # linear interpolation from wikipedia: https://en.wikipedia.org/wiki/Linear_interpolation
        # y = (y0 * (x1 - x) + y1  * (x - x0))/(x1 - x0)
        return (y0 * (x1 - searched_x) + y1 * (searched_x - x0)) / (x1 - x0)

    def get_y_at(self, searched_x):
        return self.get_value_at(self.x, self.y, searched_x)

    def get_x_at(self, searched_y):
        return self.get_value_at(self.y, self.x, searched_y)

    def integrate(self):
        summe = 0
        for i in range(0, len(self.x) - 1):
            width = (self.x[i + 1] - self.x[i])
            height = (self.y[i + 1] + self.y[i]) / 2
            summe += width * height
        return summe

    def peak_y(self):
        peak = min(self.y)  # min instead of max, because positive voltage * negative current = negative power peak
        return self.x[self.y.index(peak)], peak

    @property
    def data(self):
        return zip(self.x, self.y)

    @property
    def plot_data(self):
        return self.x, self.y

    def __imul__(self, other):
        if isinstance(other, Data2D):
            # get the overlapping range:
            x_min, x_max = max(self.x[0], other.x[0]), min(self.x[-1], other.x[-1])
            xs = [x for x in sorted(self.x + other.x) if x_min <= x <= x_max]
            ys = [self.get_y_at(x) * other.get_y_at(x) for x in xs]
            self.x, self.y = xs, ys
        else:
            self.y = [y * other for y in self.y]
        return self

    def __mul__(self, other):
        re = Data2D(self.x, self.y)
        re *= other
        return re

    def __isub__(self, other):
        if isinstance(other, Data2D):
            # get the overlapping range:
            x_min, x_max = max(self.x[0], other.x[0]), min(self.x[-1], other.x[-1])
            xs = [x for x in sorted(self.x + other.x) if x_min <= x <= x_max]
            ys = [self.get_y_at(x) - other.get_y_at(x) for x in xs]
            self.x, self.y = xs, ys
        else:
            self.y = [y - other for y in self.y]
        return self

    def __sub__(self, other):
        re = Data2D(self.x, self.y)
        re -= other
        return re

    def __iadd__(self, other):
        if isinstance(other, Data2D):
            # get the overlapping range:
            x_min, x_max = max(self.x[0], other.x[0]), min(self.x[-1], other.x[-1])
            xs = [x for x in sorted(list(self.x) + list(other.x)) if x_min <= x <= x_max]
            ys = [self.get_y_at(x) + other.get_y_at(x) for x in xs]
            self.x, self.y = xs, ys
        else:
            self.y = [y + other for y in self.y]
        return self

    def __add__(self, other):
        re = Data2D(self.x, self.y)
        re += other
        return re

    def __eq__(self, other):
        eps = 1e-16  # max allowed difference
        for s_x, o_x in zip(self.x, other.x):
            if eps < s_x - o_x < eps:
                return False
        for s_y, o_y in zip(self.y, other.y):
            if eps < s_y - o_y < eps:
                return False
        return True


def read_csv(filename, sep="\t", comment="#"):
    with open(filename, "r") as f:
        lines = f.readlines()
    res = []
    index = 0
    for line in lines:
        if line.startswith(comment):
            continue
        res.append([float(num) for num in line.split(sep)])
        index += 1
    return zip(*res)


def solar_energy_to_photon_count_to_charge(solar_power: Data2D):
    def factor(lambda_nm):
        """returns the factor for a given wavelength to turn the sun power into the number of photons,
        and then into charge with the assumption that every photon carries one elemental charge"""
        # return lambda_nm * 1.602176634e-19 / 1240  # C*nm / eV*nm
        return lambda_nm / 1240  # e*nm / eV*nm = C*nm / J*nm, no 1.6e-19 factors needed, because they cancel out

    y = [sun_y * factor(sun_x) for sun_x, sun_y in solar_power.data]
    return Data2D(solar_power.x, y)


def multiply_eqe_to_solar_spectrum(cell: Data2D, sun: Data2D):
    return cell * sun


def combine_jv_curves(c1: Data2D, c2: Data2D):
    summe = Data2D(c1.y, c1.x) + Data2D(c2.y, c2.x)
    return Data2D(summe.y, summe.x)


def jv_to_power(cell):
    voltage_unity_curve = Data2D(cell.x, cell.x)
    return cell * voltage_unity_curve


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
correction_factor = bottom_cell_current_integrated / (top_cell_current_integrated + bottom_cell_current_integrated + bottom_cell_filtered_current_integrated)
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
