        self.o_balls = [O(random.random() * screenwidth, random.random() * screenheight) for i in range(5)]
        self.c_balls = [C(random.random() * screenwidth, random.random() * screenheight) for i in range(5)]
        self.h_balls = [H(random.random() * screenwidth, random.random() * screenheight) for i in range(5)]