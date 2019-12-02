from fuel_requirements import get_fuel_requirements
from fuel_requirements import FILE

# So, for each module mass, calculate its fuel and add it to the total.
# Then, treat the fuel amount you just calculated as the input mass and repeat the process,
# continuing until a fuel requirement is zero or negative. For example:
#
# A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0,
# which would call for a negative fuel), so the total fuel required is still just 2.
# At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2).
# 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel.
# So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
# The fuel required by a module of mass 100756 and its fuel is:
# 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
# What is the sum of the fuel requirements for all of the modules on your
# spacecraft when also taking into account the mass of the added fuel?


def get_fuel_requirements_for_fuel(fuel_mass, total_fuel=0):
    fuel = get_fuel_requirements(fuel_mass)
    if fuel <= 0:
        return total_fuel
    return get_fuel_requirements_for_fuel(fuel, fuel + total_fuel)


def get_total_fuel_requirements(filename):
    total = 0
    with open(filename) as masses:
        for mass in masses:
            fuel_requirements = get_fuel_requirements(int(mass))
            total += fuel_requirements + get_fuel_requirements_for_fuel(fuel_requirements)
    return total


print(get_total_fuel_requirements(FILE))
