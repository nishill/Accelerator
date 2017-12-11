import matplotlib.pyplot as plt
import json

def main():

  with open('data.json', 'r') as fp:
  #with open('data.random.json', 'r') as fp:
    data = json.load(fp)

  #print data["chr8:9757574-9760839"]
  print data["chr8:26240974-26247876"]   
 
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
  chi = plt.hist(chimps, alpha = 0.6,bins=1000 )
  ora = plt.hist(orangs,alpha = 0.6,bins=1000 )
  gor = plt.hist(gorillas,alpha = 0.6,bins=1000 )
  rhe = plt.hist(rhesus,alpha = 0.6,bins=1000 ) 

  plt.legend(["Chimpanmzee", "Orangutan", "Gorilla","Rhesus Macaque"])

  plt.xlim(0.0,0.2)

  plt.title("Substitution Rates for Candidate HARs on chr8p for Primates")
  #plt.title("Substitution Rates of Random Regions on chr8p for Primates")
  plt.xlabel("Substitution Rate")
  plt.ylabel("Occurence")

  #plt.show()
	
if __name__=="__main__":
  main()
