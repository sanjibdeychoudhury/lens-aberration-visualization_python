# Determination of Spherical Aberration of A Singlet using Python
import numpy as np
import matplotlib.pyplot as plt

# Lens Maker's formula
def calculate_focal_length(R1, R2, t, n):
    return 1 / ((n - 1) * (1 / R1 - 1 / R2 + (n - 1) * t / (n * R1 * R2)))

# Chromatic Aberration calculation
def chromatic_aberration(focal_d, n_d, V, wavelength, R1, R2, t):
    n_lambda = n_d + ((n_d - 1) / V) * (wavelength - 589)
    focal_lambda = calculate_focal_length(R1, R2, t, n_lambda)
    return abs(focal_d - focal_lambda)

# Spherical Aberration calculation
def spherical_aberration(wavelengths, R1, R2, t, n_d, V):
    sa_values = []
    focal_d = calculate_focal_length(R1, R2, t, n_d)
    
    for wavelength in wavelengths:
        n_lambda = n_d + ((n_d - 1) / V) * (wavelength - 589)
        focal_lambda = calculate_focal_length(R1, R2, t, n_lambda)
        paraxial_focal_length = focal_lambda
        marginal_focal_length = focal_lambda - 0.001 * (wavelength - 589)  # Simplified marginal ray effect
        sa = marginal_focal_length - paraxial_focal_length
        sa_values.append(sa)
    
    return sa_values

# Main Function
def main():
    # Input lens parameters
    R1 = float(input("Enter radius of curvature R1 (mm): "))
    R2 = float(input("Enter radius of curvature R2 (mm): "))
    t = float(input("Enter lens thickness (mm): "))
    n_d = float(input("Enter refractive index for d-line (589 nm): "))
    V = float(input("Enter Abbe number: "))

    # Define wavelength range
    wavelengths = np.linspace(400, 750, 10)  # Example: 400 nm to 750 nm in 10 steps

    # Compute focal lengths and aberrations
    focal_d = calculate_focal_length(R1, R2, t, n_d)
    chromatic_aberrations = [chromatic_aberration(focal_d, n_d, V, wl, R1, R2, t) for wl in wavelengths]
    sa_values = spherical_aberration(wavelengths, R1, R2, t, n_d, V)

    # Find maximum values for the bar graph
    max_chromatic_aberration = max(chromatic_aberrations)
    max_spherical_aberration = max(sa_values)

    # Plot chromatic focal shift
    plt.figure(figsize=(8, 5))
    plt.plot(wavelengths, [focal_d - ca for ca in chromatic_aberrations], label="Chromatic Focal Shift (μm)")
    plt.title("Chromatic Focal Shift")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Focal Shift (μm)")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Plot spherical aberration variation
    plt.figure(figsize=(8, 5))
    plt.plot(wavelengths, sa_values, label="Spherical Aberration (mm)")
    plt.title("Spherical Aberration Variation")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Spherical Aberration (mm)")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Plot bar graph for max aberrations
    plt.figure(figsize=(6, 4))
    aberration_labels = ["Max Spherical Aberration (mm)", "Max Chromatic Aberration (mm)"]
    max_values = [max_spherical_aberration, max_chromatic_aberration]
    colors = ["blue", "orange"]
    plt.bar(aberration_labels, max_values, color=colors)

    # Annotate the bars with their values
    for i, value in enumerate(max_values):
        plt.text(i, value + 0.01, f"{value:.2f}", ha="center", fontsize=12, color="black")

    plt.title("Maximum Aberrations")
    plt.ylabel("Aberration (mm)")
    plt.grid(axis="y")
    plt.show()

if __name__ == "__main__":
    main()
