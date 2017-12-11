import sys
import matplotlib.pyplot as plt

def main():

	scores = []
	while True:

		line = sys.stdin.readline().strip().split()
		if not line: break
		score = float(line[4])
		scores.append(score)
		if score > 0 :
	
			print line[0]+'\t'+line[1]+'\t'+line[2]+'\t'+line[3]+'\t'+line[4]
		
	
	plt.hist(scores)
	plt.xlim(-300,90)
	plt.xlabel("Candidate HAR Log Odds Scores")
	plt.ylabel("Number of regions with score")
	plt.show()

if __name__=="__main__":
	main()
