import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class HindmarshRose:
    """
    Creates a HindmarshRose model.
    """
    def __init__(self, **kwargs):
        """
        Initializes the model.

        Args:
            I (int, float): External current.
            a (int, float): Positive parameter.
            b (int, float): Positive parameter.
            c (int, float): Positive parameter.
            d (int, float): Positive parameter.
            r (int, float): Positive parameter.
            s (int, float): Positive parameter.
            x1 (int, float): Resting potential.
            dt (int, float): Simulation step.
            time (int): Total time for the simulation.
        """
        self.I = kwargs.get("I", 1)
        self.a = kwargs.get("a", 0.5)
        self.b = kwargs.get("b", 0.5)
        self.c = kwargs.get("c", 0.5)
        self.d = kwargs.get("d", 0.5)
        self.r = kwargs.get("r", 1)
        self.s = kwargs.get("s", 1)
        self.x1 = kwargs.get("x1", -1)
        self.dt = kwargs.get("dt", 0.01)
        self.time = kwargs.get("time", 100)
        self.check_parameters()

    def __repr__(self):
        """
        Visualize model parameters when printing.
        """
        return (f"HindmarshRose(a={self.a}, b={self.b}, c={self.c}, d={self.d}, dt={self.dt}, time={self.time})")

    def check_parameters(self):
        """
        Verify the data types of the inputs
        """
        assert isinstance(self.I, (int, float)), \
            "The current (I) has to be a number."
        assert isinstance(self.a, (int, float)), \
            "The parameter a has to be a number."
        assert isinstance(self.b, (int, float)), \
            "The parameter b has to be a number."
        assert isinstance(self.c, (int, float)), \
            "The parameter c has to be a number."
        assert isinstance(self.d, (int, float)), \
            "The parameter d has to be a number."
        assert isinstance(self.r, (int, float)), \
            "The parameter r has to be a number."
        assert isinstance(self.x1, (int, float)), \
            "The parameter x1 has to be a number."
        assert isinstance(self.s, (int, float)), \
            "The parameter s has to be a number."
        assert isinstance(self.dt, (int, float)), \
            "The step (dt) has to be a number."
        assert isinstance(self.time, (int, float)), \
            "The time has to be a number."

    @property
    def tvec(self):
        """
        Calculates a time vector tvec.
        """
        return np.arange(0, self.time, self.dt)

    def system_equations(self, X, t, I):
        """
        Defines the equations of the dynamical system for integration.
        """
        return [X[1] - self.a * (X[0]**3) + self.b * (X[0]**2) - X[2] + I,
                self.c - self.d * (X[0]**2) - X[1],
                self.r * (self.s * (X[0] - self.x1) - X[2])]

    def run(self, X0=[0, 0, 0], I=None):
        """
        Run the model by integrating the system numerically.
        """
        if I is None:
            I = self.I
        else:
            self.I = I
        X = odeint(self.system_equations, X0, self.tvec, (I,))
        self.x, self.y, self.z = X[:, 0], X[:, 1], X[:, 2]

    def plot(self):
        """
        Plot the membrane potential over time as well as the activation and innactivation of the channels.
        """
        f, ([ax1, ax2, ax3]) = plt.subplots(1, 3, figsize=(13, 3), tight_layout=True)
        # Plot x(t)
        ax1.plot(self.tvec, self.x, color='royalblue')
        ax1.set_title("x", fontsize=15)
        ax1.set_xlabel("time [ms]", fontsize=12)
        ax1.set_ylabel("x(t)", fontsize=12)
        ax1.grid(alpha=0.3)
        # Plot y(t)
        ax2.plot(self.tvec, self.y, color='lightcoral')
        ax2.set_title("y", fontsize=15)
        ax2.set_xlabel("time [ms]", fontsize=12)
        ax2.set_ylabel("y(t)", fontsize=12)
        ax2.grid(alpha=0.3)
        # Plot z(t)
        ax3.plot(self.tvec, self.z, color='goldenrod')
        ax3.set_title("z", fontsize=15)
        ax3.set_xlabel("time [ms]", fontsize=12)
        ax3.set_ylabel("z(t)", fontsize=12)
        ax3.grid(alpha=0.3)
        plt.show()

    def phase_plane(self):
        """
        Plots the phase plane of the system.
        """
        f, ([ax1, ax2]) = plt.subplots(1, 2, figsize=(13, 3), tight_layout=True)
        # Plot y over x
        ax1.plot(self.x, self.y, color='royalblue')
        ax1.set_xlabel("x", fontsize=12)
        ax1.set_ylabel("y", fontsize=12)
        ax1.grid(alpha=0.3)
        # Plot z over x
        ax2.plot(self.x, self.z, color='royalblue')
        ax2.set_xlabel("x", fontsize=12)
        ax2.set_ylabel("z", fontsize=12)
        ax2.grid(alpha=0.3)
        plt.show()
