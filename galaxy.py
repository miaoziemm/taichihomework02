import taichi as ti
from celestial_objects import Star, Planet, Black_hole

if __name__ == "__main__":

    ti.init(arch=ti.cpu)

    # control
    paused = False
    export_images = False
    freeze=True
    k=1
    k_max=100

    # stars and planets
    stars = Star(N=2, mass=1000)
    stars.initialize(0.5, 0.5, 0.2, 10)
    planets = Planet(N=2000, mass=1)
    planets.initialize(0.5, 0.5, 0.4, 10)
    Blackhole=Black_hole(N=1, mass=100000)
    

    # GUI
    my_gui = ti.GUI("Galaxy", (800, 800))
    h = 5e-5 # time-step size
    i = 0
    while my_gui.running:

        for e in my_gui.get_events(ti.GUI.PRESS):
            if e.key == ti.GUI.ESCAPE:
                exit()
            elif e.key == ti.GUI.SPACE:
                paused = not paused
                print("paused =", paused)
            elif e.key == 'r':
                stars.initialize(0.5, 0.5, 0.2, 10)
                planets.initialize(0.5, 0.5, 0.4, 10)
                i = 0
            elif e.key == 'i':
                export_images = not export_images
            elif e.key == ti.GUI.LMB:
                x, y = e.pos
                stars.add(x, y)
            elif e.key == ti.GUI.RMB:
                x, y = e.pos
                planets.add(x, y)
            elif e.key == 'b':
                Blackhole.initialize(0.5, 0.5, 0.2, 10)
            elif e.key == 'f':
                freeze=not freeze

                

        if not paused:
            stars.computeForce(planets, Blackhole)
            planets.computeForce(stars, Blackhole)
            Blackhole.blackhole_absorb(stars, planets)
            if not freeze:
                stars.freeze()
                planets.freeze()
                Blackhole.freeze()
            # Blackhole.update_black_hole()
            for celestial_obj in (stars, planets):
                celestial_obj.update(h)
            i += 1

        stars.display(my_gui, radius=10, color=0xffd500)
        planets.display(my_gui)
        Blackhole.display(my_gui, radius=15, color=0xff00ff)
        if export_images:
            my_gui.show(f"images\output_{i:05}.png")
        else:
            my_gui.show()