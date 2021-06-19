class Data2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_y_at(self, searched_x):
        # if we don't span this range, return 0
        if searched_x < self.x[0] or searched_x > self.x[-1]:
            return 0
        # if we have the element, return it
        if searched_x in self.x:
            return self.y[self.x.index(searched_x)]
        # now we do linear interpolation
        x0, x1, y0, y1 = (0, 0, 0, 0)
        for x, y in zip(self.x, self.y):
            if x > searched_x:
                x1, y1 = x, y
                break
            x0, y0 = x, y
        # linear interpolation from wikipedia: https://en.wikipedia.org/wiki/Linear_interpolation
        # y = (y0 * (x1 - x) + y1  * (x - x0))/(x1 - x0)
        return (y0 * (x1 - searched_x) + y1 * (searched_x - x0)) / (x1 - x0)

    def integrate(self):
        summe = 0
        for i in range(1, len(self.x) - 1):
            prev_x = self.x[i - 1]
            next_x = self.x[i + 1]

            width = (next_x - prev_x) / 2
            summe += width * self.y[i]
        return summe

    @property
    def data(self):
        return zip(self.x, self.y)

    @property
    def plot_data(self):
        return self.x, self.y

    def __imul__(self, other):
        """multiply the y values with the given value"""
        self.y = [y * other for y in self.y]
        return self

    def __mul__(self, other):
        return Data2D(self.x, [y * other for y in self.y])

    def __sub__(self, other):
        y = [s_y - other.get_y_at(s_x) for s_x, s_y in self.data]
        return Data2D(self.x, y)

    def __isub__(self, other):
        self.y = [s_y - other.get_y_at(s_x) for s_x, s_y in self.data]
        return self

    def __add__(self, other):
        y = [s_y + other.get_y_at(s_x) for s_x, s_y in self.data]
        return Data2D(self.x, y)

    def __iadd__(self, other):
        self.y = [s_y + other.get_y_at(s_x) for s_x, s_y in self.data]
        return self

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
    y = [sun_y * cell.get_y_at(sun_x) for sun_x, sun_y in sun.data]
    return Data2D(sun.x, y)


cell_size = 0.1e-4  # m^2 to 0.1cm^2
ampere_to_milli_ampere = 1000  # to convert from Ampere to Milliampere

solar_spectrum = Data2D(*read_csv("sun_spectrum_direct_circumsolar.csv"))
solar_spectrum_converted = solar_energy_to_photon_count_to_charge(solar_spectrum)

eqe_bottom_cell = Data2D(*read_csv("eqe-kp115idtbr.csv"))
bottom_cell_current = multiply_eqe_to_solar_spectrum(eqe_bottom_cell, solar_spectrum_converted) * cell_size * ampere_to_milli_ampere
bottom_cell_current_integrated = bottom_cell_current.integrate()
print(f"{bottom_cell_current_integrated=}")

eqe_bottom_cell_filtered = Data2D(*read_csv("eqe-kp115idtbr-filtered.csv"))
bottom_cell_filtered_current = multiply_eqe_to_solar_spectrum(eqe_bottom_cell_filtered, solar_spectrum_converted) * cell_size * ampere_to_milli_ampere
bottom_cell_filtered_current_integrated = bottom_cell_filtered_current.integrate()
print(f"{bottom_cell_filtered_current_integrated=}")

eqe_top_cell = Data2D(*read_csv("eqe-p3htpcbm.csv"))
top_cell_current = multiply_eqe_to_solar_spectrum(eqe_top_cell, solar_spectrum_converted) * cell_size * ampere_to_milli_ampere
top_cell_current_integrated = top_cell_current.integrate()
print(f"{top_cell_current_integrated=}")

# we were given the following to calculate the thickness correction factor for the top cell:
# P3HT*x = KP115filtered + (KP115-KP115filtered)*(1-x)
# => P*x = Kf + (K - Kf) * (1-x)
# => x = K / (P + K + Kf)
x = bottom_cell_current_integrated / (top_cell_current_integrated + bottom_cell_current_integrated + bottom_cell_filtered_current_integrated)
print(f"{x=}")

top_cell_current_scaled = top_cell_current * x
print(f"{top_cell_current_scaled.integrate()=}")
bottom_cell_current_scaled = bottom_cell_filtered_current + (bottom_cell_current - bottom_cell_filtered_current) * (1 - x)
print(f"{bottom_cell_current_scaled.integrate()=}")

assert bottom_cell_current == bottom_cell_filtered_current + (bottom_cell_current - bottom_cell_filtered_current)