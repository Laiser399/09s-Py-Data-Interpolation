from sympy import S, \
    Mul, Abs, factorial, \
    diff, solve


class LagrangeInterpolator(object):
    def __init__(self, n: int, a: float, b: float, f_x_sym, x_sym):
        self.f = f_x_sym
        self.x = x_sym
        self.n = S(n)
        self.points_count = self.n + 1
        self.a, self.b = S(a), S(b)

        delta = (self.b - self.a) / self.n
        self.x_arr = [(self.a + delta * i) for i in range(self.points_count)]
        self.y_arr = [self.f.subs(self.x, x_i) for x_i in self.x_arr]

        self.interpolation_result = self.interpolate()

        self.M_np1 = self.calculate_M_np1()

        self.real_error = self.calculate_real_error()
        self.max_error = self.calculate_max_error()

    def interpolate(self):
        sum_elements = [self.y_arr[i] * self.make_l(i)
                        for i in range(self.points_count)]
        return sum(sum_elements)

    def make_l(self, i):
        fractions = [(self.x - self.x_arr[j]) / (self.x_arr[i] - self.x_arr[j])
                     for j in range(self.points_count)
                     if i != j]
        return Mul(*fractions)

    def calculate_M_np1(self):
        df_np1 = diff(self.f, self.x, self.n + 1)
        df_np2 = diff(df_np1, self.x)

        res = solve(df_np2, self.x)
        res = [r for r in res if self.a <= r <= self.b]
        res.append(self.a)
        res.append(self.b)

        return max([Abs(df_np1.subs(self.x, r)) for r in res])

    def calculate_real_error(self):
        return Abs(self.interpolation_result - self.f)

    def calculate_max_error(self):
        multiply_elements = [self.x - x_i for x_i in self.x_arr]
        return self.M_np1 / factorial(self.n + 1) * Abs(Mul(*multiply_elements))
