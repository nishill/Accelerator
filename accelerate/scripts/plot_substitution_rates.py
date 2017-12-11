import matplotlib.pyplot as plt
import json

def main():

  with open('data.json', 'r') as fp:
    data = json.load(fp)


  regions = data.keys()
  chimps = []
  orangs = []
  gorillas = []
  rhesus = []
  for region in regions:
  
      chimps.append(data[region]["panTro4"])
      orangs.append(data[region]["ponAbe2"])
      gorillas.append(data[region]["gorGor3"]) 
      rhesus.append(data[region]["rheMac3"]) 

  region_range = range(0, len(regions))
  chi = plt.plot(region_range, chimps,alpha=0.6 )
  ora = plt.plot(region_range, orangs,alpha=0.6)
  gor = plt.plot(region_range, gorillas,alpha=0.6)
  rhe = plt.plot(region_range, rhesus,alpha=0.6) 

  plt.legend(["Chimp.", "Orang.", "Goril.","Rhesu."])

  plt.title("Substitution rates for regions on chr8p for Primates")
  plt.xlabel("Region")
  plt.ylabel("Substitution Rate")

  plt.show()
	
if __name__=="__main__":
  main()
