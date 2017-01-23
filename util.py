# Module: util.py

def exit_error(error_message):
    print error_message
    exit(1)

def split(arr, size):
	arrs = []
	while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr = arr[size:]
	arrs.append(arr)
	return arrs
