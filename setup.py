from setuptools import setup
import os

data_files = []

package = "src/rstatmon/"
dst = ["static", "templates", "data", "config"]

for d in dst:
    s = os.path.join(package, d)
    for root, dirs, files in os.walk(s):
        root_files = [os.path.join(root, i) for i in files]
        data_files.append((root, root_files))


setup(
    data_files=data_files,
)
