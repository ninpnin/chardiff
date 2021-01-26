#!/usr/bin/python3
import sys
import diff_match_patch as dmp_module

class bcolors:
    RESET = '\033[0m'
    ADD = '\033[92m'
    DELETE = '\033[91m'
    INDEX = '\033[36m'
    BOLD = "\033[1m"

def chardiff(f1,f2):
	print(bcolors.BOLD + "diff", "--git", f2)
	print(bcolors.BOLD + "index ???")
	print(bcolors.BOLD + "---", f1.split("/")[-1])
	print(bcolors.BOLD + "+++", f2.split("/")[-1])
	s1 = open(f1).read()
	s2 = open(f2).read()
	dmp = dmp_module.diff_match_patch()
	diff = dmp.diff_main(s1, s2)
	dmp.diff_cleanupSemantic(diff)
	str1 = ""
	str2 = ""
	for ix, piece in enumerate(diff):
		change, elem = piece
		if change > 0:
			str1 += elem
			if elem.strip() == "":
				elem = elem.replace(" ", "_")
			elem = elem.replace("\n", "\\n\n+")
			print(bcolors.ADD + "+" + elem, end='')
		elif change < 0:
			str2 += elem
			elem = elem.replace("\n", "\\n\n-")
			print(bcolors.DELETE + "-" + elem, end='')
		else:
			str1 += elem
			str2 += elem
			split = elem.split("\n")
			split = [s for s in split if len(s) > 0]
			if len(split) >= 2:
				if ix > 0:
					if "\n" == elem[0]:
						print()
					print(bcolors.RESET + split[0])
					lastelem = split[-1]
				if ix < len(diff) - 1:
					ix1 = str1.count("\n") + 1
					ix2 = str2.count("\n") + 1
					print(bcolors.INDEX + "@@ +" + str(ix1) +", -" + str(ix2) +" @@")
					print(bcolors.RESET + split[-1],  end='')
					if "\n" == elem[-1]:
						print()
			else:
				print(bcolors.RESET + elem, end='')
	print(bcolors.RESET)

def main():
	assert len(list(sys.argv)) >= 3, "Provide files to diff"
	f1 = sys.argv[2]
	f2 = sys.argv[1]
	chardiff(f1, f2)

if __name__ == '__main__':
	main()