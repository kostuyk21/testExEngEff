import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


class CheckResidual:
    def __init__(self, filename): # Made all var and methods protected just in case
        self._pattern_time = r"^Time" 
        self._pattern_final_residual = r"Final residual = [0-9]" 
        self._filename = filename
        self._raw_data = self._read_file()
        self._data = self._get_residual_data()
        self._time = self._get_time()
        self._p_rgh = self._get_residual_for_p_rgh()
        self._k = self._get_residual_for_k()
        self._omega = self._get_omega_residual()

    def _read_file(self): # Can be outside of a class 
        try:
            with open(self._filename) as fp:
                lines = fp.readlines()
            return [line for line in lines]
        except FileNotFoundError:
            raise FileNotFoundError  # Error Handling if needed

    def _get_time(self): # get time from file
        time = [line.split()[2] for line in self._raw_data if re.search(self._pattern_time, line)][1:]# Clear data and get what we need
        return np.array(time, dtype="float") 

    def _get_residual_data(self):#split data to final residual data
        return [line.replace(",", " ").split() for line in self._raw_data if re.findall(self._pattern_final_residual, line)]

    def _get_residual_for_p_rgh(self): #get last p_rgh values from raw data
        final_residual_for_p_rgh = [float(line[0][11]) for line in zip(self._data, self._data[1:] + [0]) if line[0][3] == "p_rgh" if line[1][0] == "smoothSolver:"] # can be slow 
        return np.array(final_residual_for_p_rgh)

    def _get_residual_for_k(self):#get k values from raw data
        return np.array([float(line[11]) for line in self._data if line[3] == "k"])

    def _get_omega_residual(self): #get omega values from raw data
        return np.array([float(line[11]) for line in self._data if line[3] == "omega"])

    def _generate_graph(self): # Generates graph as instructed
        fig = plt.figure(figsize=(10, 7))
        plt.title("Residue profile")
        plt.yscale("log")
        plt.xlabel("Time")
        plt.ylabel("Final residual")
        plt.plot(self._time, self._p_rgh, label="p_rgh")
        plt.plot(self._time, self._omega, label="omega")
        plt.plot(self._time, self._k, label="k")
        plt.legend()
        plt.show()

    def _save_data(self): # Creates pandas DataFrame and saves to csv file
        df = pd.DataFrame(
            {"Time": self._time, 
             "p_rgh": self._p_rgh, 
             "omega": self._omega, 
             "k": self._k}
        )
        df.to_csv("residue_profile.csv", index=False, encoding="utf-8")

    def run(self): 
        self._save_data()
        self._generate_graph()


if __name__ == "__main__":
    obj = CheckResidual("log.run")
    obj.run()