import taichi as ti


@ti.data_oriented
class CelestialObject:
    def __init__(self, N, mass) -> None:
        # constants
        self.G = 1
        self.PI = 3.1415926

        # celestial object related fields
        self.n = N
        self.m = mass
        self.max_ball = 5000

        self.ball_num = ti.field(dtype=ti.i32, shape=())
        self.mass=ti.field(dtype=ti.i32, shape=())
        self.mass=self.m
        self.pos = ti.Vector.field(2, ti.f32, shape=self.max_ball)
        self.vel = ti.Vector.field(2, ti.f32, shape=self.max_ball)
        self.force = ti.Vector.field(2, ti.f32, shape=self.max_ball)

    def display(self, gui, radius=2, color=0xffffff):
        num=self.ball_num[None]
        gui.circles(self.pos.to_numpy()[0:num:1], radius=radius, color=color)


    @ti.func
    def clearForce(self):
        for i in self.force:
            self.force[i] = ti.Vector([0.0, 0.0])

    @ti.kernel
    def initialize(self, center_x: ti.f32, center_y: ti.f32, size: ti.f32, init_speed: ti.f32):
        self.ball_num[None] = self.n
        for i in range(self.ball_num[None]):
            if self.n == 1:
                self.pos[i] = ti.Vector([center_x, center_y])
                self.vel[i] = ti.Vector([0.0, 0.0])
            else:
                theta, r = self.generateThetaAndR(self.PI, i, self.n)
                offset_dir = ti.Vector([ti.cos(theta), ti.sin(theta)])
                center = ti.Vector([center_x, center_y])
                self.pos[i] = center + r * offset_dir * size
                self.vel[i] = ti.Vector([-offset_dir[1], offset_dir[0]]) * init_speed

    @ti.kernel
    def computeForce(self, stars: ti.template(), blackhole: ti.template()):
        self.clearForce()
        G = 1.0
        for i in range(self.ball_num[None]):
            p = self.pos[i]

            for j in range(self.ball_num[None]):
                if i != j:
                    diff = self.pos[j] - p
                    r = diff.norm(1e-2)
                    self.force[i] += G * self.mass * self.mass * diff / r ** 3

            for j in range(stars.ball_num[None]):
                diff = stars.Pos()[j] - p
                r = diff.norm(1e-2)
                self.force[i] += G * self.mass * stars.mass * diff / r ** 3
            
            for j in range(blackhole.ball_num[None]):
                diff = blackhole.Pos()[j] - p
                r = diff.norm(1e-2)
                self.force[i] += G * self.mass * blackhole.mass * diff / r ** 3 

    @ti.kernel
    def update(self, h: ti.f32):
        for i in self.vel:
            self.vel[i] += h * self.force[i] / self.mass
            self.pos[i] += h * self.vel[i]

    @ti.kernel
    def add(self, x: ti.f32, y: ti.f32):
        self.pos[self.ball_num[None]] = ti.Vector([x, y])
        self.ball_num[None] += 1

    @ti.kernel
    def freeze(self):
        self.clearForce()
        for i in range(self.ball_num[None]):
            self.vel[i]=self.vel[i]*0.95

    def Pos(self):
        return self.pos

    def Mass(self):
        return self.m

    def Number(self):
        return self.n


@ti.data_oriented
class Star(CelestialObject):
    def __init__(self, N, mass) -> None:
        super().__init__(N, mass)
        pass

    @staticmethod
    @ti.func
    def generateThetaAndR(pi, i, n):
        theta = 2 * pi * i / ti.cast(n, ti.f32)
        r = 1
        return theta, r


@ti.data_oriented
class Planet(CelestialObject):
    def __init__(self, N, mass) -> None:
        super().__init__(N, mass)
        pass

    @staticmethod
    @ti.func
    def generateThetaAndR(pi, i, n):
        theta = 2 * pi * ti.random()  # theta \in (0, 2PI)
        r = (ti.sqrt(ti.random()) * 0.4 + 0.6)  # r \in (0.6,1)    
        return theta, r            

@ti.data_oriented
class Black_hole(CelestialObject):
    def __init__(self, N, mass) -> None:
        super().__init__(N, mass)
        pass

    @staticmethod
    @ti.func
    def generateThetaAndR(pi, i, n):
        theta = 2 * pi * ti.random()  # theta \in (0, 2PI)
        r = (ti.sqrt(ti.random()) * 0.4 + 0.6)  # r \in (0.6,1)    
        return theta, r

    @ti.kernel
    def update_black_hole(self):
        self.mass+=1000000

    @ti.kernel
    def blackhole_absorb(self, stars: ti.template(), planets: ti.template()):
        for i in range(self.ball_num[None]):
            p = self.pos[i] 
            for j in range(planets.ball_num[None]):
                diff = planets.pos[j] - p
                r = diff.norm()
                if r < 0.05:
                    planets.vel[j]=ti.Vector([0, 0])
            for j in range(stars.ball_num[None]):
                diff = stars.pos[j] - p
                r = diff.norm()
                if r < 0.05:
                    stars.vel[j]=ti.Vector([0, 0])
                        
        
        

    
    
        

