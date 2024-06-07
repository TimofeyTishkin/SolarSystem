import math
from PIL import Image, ImageDraw

g = 6.6743 * 10 ** (-11)


class Sphere(object):
    dist_r = 0
    fi = 0

    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius


Sun = Sphere(1.98847 * 10 ** 30, 7 * 10 ** 8)


class Planet(Sphere):
    def __init__(self, c, b, e, radius, sun, face):
        self.c = c
        self.b = b
        self.e = e
        super().__init__(b * c / (g * e) - sun.mass, radius)
        self.a = c ** 2 / (g * (sun.mass + math.fabs(self.mass)) * (1 - e ** 2))
        self.star = sun
        self.dist_r = self.a * (1 - e)
        self.face = face

    def move(self):
        self.fi += 5*24 * 3600 * self.c / self.dist_r ** 2
        self.dist_r = self.c ** 2 / ((1 + self.e * math.cos(self.fi)) * g * (self.star.mass + self.mass))

    def set_fi(self, fi):
        self.fi = fi

    def set_mass(self, mass):
        self.e = self.e * self.mass / mass
        self.mass = mass
        self.a = self.c ** 2 / (g * (self.star.mass + self.mass) * (1 - self.e ** 2))
    # def set_speed(self, speed):
    #    speed_before = math.sqrt(g*(self.star.mass+self.mass)/self.a)
    #    new_a =


class Planets:
    SS_planets = [Planet(2713027468934255.0, 10059.343727731286, 0.205635930, 2440000, Sun,
                         ".\\planets\\Mercury.png"),
                  Planet(3789521934243586.0, 238.14985283485285, 0.006800000, 6052000, Sun,
                         ".\\planets\\Venus.png"),
                  Planet(4455184162735938.0, 497.81597920753470, 0.016711230, 6371000, Sun,
                         ".\\planets\\Earth.png"),
                  Planet(5476133135283714.0, 2263.447107031402, 0.093394100, 3390000, Sun,
                         ".\\planets\\Mars.png"),
                  Planet(1.0157688310364054*10**16, 637.8838856305948, 0.048775000, 69910000, Sun,
                         ".\\planets\\Jupiter.png"),
                  Planet(1.3753876872806482*10**16, 537.8485088173016, 0.055723219, 99000000, Sun,
                         ".\\planets\\Saturn.png"),
                  Planet(1.9520411354116510*10**16, 301.9203367587625, 0.044405586, 25365000, Sun,
                         ".\\planets\\Uranus.png"),
                  Planet(2.4446608957176252*10**16, 60.88348186930187, 0.011214269, 24625000, Sun,
                         ".\\planets\\Neptune.png")]

    @staticmethod
    def get_planet(name):
        match name:
            case "Mercury":
                return Planets.SS_planets[0]
            case "Venus":
                return Planets.SS_planets[1]
            case "Earth":
                return Planets.SS_planets[2]
            case "Mars":
                return Planets.SS_planets[3]
            case "Jupiter":
                return Planets.SS_planets[4]
            case "Saturn":
                return Planets.SS_planets[5]
            case "Uranus":
                return Planets.SS_planets[6]
            case "Neptune":
                return Planets.SS_planets[7]


def rotate(p):
    centre = 2048                           # The middle of the picture. Picture height and width are: 2 * centre
    k = (p[-1].a * (1 + p[-1].e) / centre)  # Coefficient "meters per pixel"
    while p[-1].fi <= 2 * math.pi:
        sun_radius = int(10*Sun.radius / k)  # Radius of the Sun looks like a dot without "10 *"
        im = Image.new('RGB', (centre * 2, centre * 2))  # Create a new label
        draw = ImageDraw.Draw(im)
        draw.ellipse([(centre, centre), (centre + sun_radius, centre + sun_radius)], fill="yellow")  # Drawing Sun
        for planet in p:                                  # For each planet
            x = planet.dist_r * math.cos(planet.fi) / k   # Transferring coordinates to De' Cart's coordinate system
            y = planet.dist_r * math.sin(planet.fi) / k
            p_radius = 1000*planet.radius / k           # Planet radius looks like a dot without "1000 *"
            im.paste(Image.open(planet.face).resize((int(p_radius*2), int(p_radius*1.9))),  # Pasting the planet's face:
                     (centre + int(x), centre - int(y)))  # resize it to make small enough then put in the right place
            planet.move()  # Move the planet
        images.append(im)  # Append the picture after all the planets been moved and drawn
    for plan in p:
        plan.set_fi(0)
        plan.dist_r = plan.a * (1 - plan.e)  # Return everything back (not important)


P = [Planets.get_planet("Mercury"), Planets.get_planet("Venus"),
     Planets.get_planet("Earth"), Planets.get_planet("Mars")
     # Planets.get_planet("Jupiter"), Planets.get_planet("Saturn"),
     # Planets.get_planet("Uranus"), Planets.get_planet("Neptune")
     ]
images = []
rotate(P)
images[0].save(
        '.\\output\\Earth_rotation.gif',
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=40,
        loop=0
    )
