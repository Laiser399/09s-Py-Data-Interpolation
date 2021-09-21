import numpy as np
import matplotlib.pyplot as plt
from LagrangeInterpolator import LagrangeInterpolator


def make_plot(interpolator: LagrangeInterpolator):
    x = interpolator.x
    a, b = interpolator.a, interpolator.b
    f = interpolator.f

    x_grid = np.arange(a, b, 0.1)

    f_grid = np.array([f.subs(x, x_arg) for x_arg in x_grid])

    interp_res = interpolator.interpolation_result
    interpolation_result_grid = np.array([interp_res.subs(x, x_arg).n(4)
                                          for x_arg in x_grid])

    plt.plot(x_grid, f_grid, color='orange')
    plt.plot(x_grid, interpolation_result_grid, color='blue')
    plt.grid()


def compare_errors(filename, interpolator: LagrangeInterpolator, real_error, steps_count):
    x = interpolator.x
    a, b = interpolator.a, interpolator.b
    max_error = interpolator.max_error

    step = (b - a) / steps_count
    is_ok = True
    with open(filename, 'w') as file:
        for i in range(steps_count):
            x_arg = a + step * i
            real_error_res = real_error.subs(x, x_arg).n(10)
            max_error_res = max_error.subs(x, x_arg).n(10)
            if real_error_res <= max_error_res:
                file.write(f'ok: {real_error_res}\t<=\t{max_error_res}\n')
            else:
                is_ok = False
                file.write(f'not ok: {real_error_res}\t>\t{max_error_res}\n')

    return is_ok


