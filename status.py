import GPUtil as gputil
import psutil

gpu = gputil.getGPUs()

for item in gpu:
    gpu_usage = item.load*100
    gpu_memory = item.memoryUsed
    gpu_temp = item.temperature

ram = psutil.virtual_memory()
disk = psutil.disk_usage('/')

print(f"gpu: {round(gpu_usage)}%")
print(f"gpu mem: {round(gpu_memory)}MiB")
print(f"temp: {gpu_temp}C")
print(f"ram used: {round(ram.used/(1024**3))}GiB")
print(f"disk free: {round(disk.free/(1024**3))}GiB")
