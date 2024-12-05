import matplotlib as plt
from Zonnecel_experiment import ZonnecelExperiment

# from Controller import list_devices


def plot_current_vs_voltage():
    """Plots the current versus voltage for the LED with error bars and saves data to CSV."""
    experiment = ZonnecelExperiment("ASRL12::INSTR")

    voltages, currents, voltages_uncertainty, currents_uncertainty = experiment.scan(
        n=2, start=0, stop=1023
    )

    print(voltages)

    plt.errorbar(
        voltages,
        currents,
        xerr=voltages_uncertainty,
        yerr=currents_uncertainty,
        fmt="o",
        ecolor="red",
        capsize=5,
        markersize=2,
    )
    plt.xlabel("voltage LED U (V)")
    plt.ylabel("current LED I (A)")
    plt.title("current versus voltage")
    plt.savefig("plot.png")


plot_current_vs_voltage()
