import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
class CheckResidual:
    
    def __init__(self, filename):
        self.pattern_time = r"^Time"
        self.pattern_final_residual = r"Final residual = [0-9]"
        self.filename = filename
        self.raw_data = self.getData()
        self.data = self.getResidualData()
        self.time = self.getTime()
        self.p_rgh = self.__getResidualFor_p_rgh()
        self.k = self.__getResidualFor_k()
        self.omega = self.__getOmegaResidual()

    def readFile(self):
        try: 
            with open(self.filename) as fp:
                lines = fp.readlines()
            return [line for line in lines]
        except FileNotFoundError:
            raise FileNotFoundError # Error Handling
            
    def getData(self):
        return self.readFile()
        
    def getTime(self):
        time = [line.split()[2] for line in self.raw_data if re.search(self.pattern_time,line)][1:] #Clear data and get what we need
        return  np.array(time, dtype='float')
    
    def getResidualData(self):
        return [line.replace(',', ' ').split() for line in self.raw_data if re.findall(self.pattern_final_residual,line)]
    
    def __getResidualFor_p_rgh(self):
        final_residual_for_p_rgh = [float(line[0][11]) for line in zip(self.data, self.data[1:] + [0])  if line[0][3] == 'p_rgh' if line[1][0] == "smoothSolver:"]# slower
        return np.array(final_residual_for_p_rgh)
    
    def __getResidualFor_k(self):
        return np.array([float(line[11]) for line in self.data if line[3] == 'k'])
    
    def __getOmegaResidual(self):
        return np.array([float(line[11]) for line in self.data if line[3] == 'omega'])
    
    def __writeGraph(self):
        fig = plt.figure(figsize=(10,7))
        plt.title("Residue profile")
        plt.yscale("log")
        plt.xlabel("Time")
        plt.ylabel("Final residual")
        plt.plot(self.time, self.p_rgh, label = "p_rgh")
        plt.plot(self.time, self.omega, label = "omega")
        plt.plot(self.time, self.k, label = "k")
        plt.legend()
        plt.show()
    
    def __saveData(self):
        df = pd.DataFrame({"Time":self.time,
                  "p_rgh":self.p_rgh,
                  "omega":self.omega,
                  "k":self.k})
        df.to_csv("residue_profile.csv", index=False, encoding='utf-8')
        
    def run(self):
        
        self.__saveData()
        self.__writeGraph()
        
    
if __name__ == "__main__":
    obj = CheckResidual("log.run")
    obj.run()