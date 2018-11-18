git_address = "https://github.com/Akbar30Bill/pyGrabber.git"
if __name__ == "__main__":
	import os
	import subprocess
	git_address = "https://github.com/Akbar30Bill/pyGrabber.git"
	subprocess.call(["git" , "clone" , git_address])
	print("replacing new files")
	subprocess.call(["cp" , "-r" , "pyGrabber/pyGrabber.py" , "." ])
	if (input("update update script (y/n) ? ") == "y" or "Y"):
		print("replacing update script")
		subprocess.call(["cp" , "-r" , "pyGrabber/update.py" , "." ])
	print("removing cloned files")
	subprocess.call(["rm" , "-rf" , "pyGrabber/"])
	print("script updated ")
	# subprocess.call(["git" , "pull"])

