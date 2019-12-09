INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
CENTER_ID = 'COM'


class SpaceObject:
    """ Represents a space object. Instances are equivalent if they have they same name."""

    def __init__(self, id_, primary=None, satellites=None):
        self.id_ = id_
        self.primary = primary
        self.satellites = satellites or []

    # def __repr__(self):
    #     return '<SpaceObject id: {}, primary: {}, satellites: {}>'.format(self.id_, self.primary, self.satellites)

    def __eq__(self, other):
        if not isinstance(other, SpaceObject):
            return False
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)


class OrbitMap:
    def __init__(self, center=None):
        self.center = center
        # Space objects that do not have a primary
        self.floating_orbits = set()

    def get_space_object_from_floating_orbits_by_id(self, id_, is_remove_on_found=False):
        for orbit in self.floating_orbits:
            space_object = self.get_space_object_from_orbit_by_id(id_, orbit)
            if space_object is not None:
                if is_remove_on_found:
                    self.floating_orbits.remove(space_object)
                return space_object
        return None

    @staticmethod
    def get_space_object_from_orbit_by_id(id_, orbit):
        current_space_object = orbit
        space_objects_to_scan = []
        while current_space_object:
            space_objects_to_scan = space_objects_to_scan + current_space_object.satellites
            if current_space_object.id_ == id_:
                return current_space_object
            current_space_object = space_objects_to_scan.pop() if len(space_objects_to_scan) > 0 else None
        return None

    def create_orbit(self, primary_id, satellite_id):
        primary_from_center = self.get_space_object_from_orbit_by_id(primary_id, self.center)
        primary_from_floating = self.get_space_object_from_floating_orbits_by_id(primary_id)
        primary = primary_from_center or primary_from_floating or SpaceObject(primary_id)

        satellite = self.get_space_object_from_floating_orbits_by_id(satellite_id, is_remove_on_found=True) or \
            SpaceObject(satellite_id)
        if satellite.primary:
            raise Exception("Trying to add a second primary to satellite: {} \nInvalid orbit.".format(satellite))
        else:
            satellite.primary = primary

        primary.satellites.append(satellite)

        if primary_id == CENTER_ID:
            if not self.center:
                self.center = primary
            else:
                raise Exception('Center of universe already exists. What are you trying to do here?')

        if not primary_from_center:
            self.floating_orbits.add(primary)

    def count_total_orbits(self):
        total_orbit_count = 0

        space_objects_to_scan = [(self.center, 0)]
        while space_objects_to_scan:
            current_space_object, orbits_on_path = space_objects_to_scan.pop()
            if not current_space_object:
                raise Exception("Found empty space object.")

            total_orbit_count += orbits_on_path
            space_objects_to_scan = space_objects_to_scan + \
                [(space_object, orbits_on_path + 1) for space_object in current_space_object.satellites]

        return total_orbit_count


def get_solution():
    orbit_map = OrbitMap()

    with open(INPUT) as orbit_codes:
        for orbit_code in orbit_codes:
            orbit_code = orbit_code.strip()
            primary_id, satellite_id = orbit_code.split(')')
            orbit_map.create_orbit(primary_id, satellite_id)

    print(orbit_map.count_total_orbits())


get_solution()
