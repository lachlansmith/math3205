import subprocess


if __name__ == "__main__":

    for i in range(501):
        p = subprocess.Popen(['python3', './main.py', '-h', '-p', f'-i {i}', '-v'])
        try:
            p.wait(30)
        except subprocess.TimeoutExpired:
            p.kill()
