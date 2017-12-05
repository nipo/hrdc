from setuptools import setup, find_packages

setup(
    name = "hrdc",
    version = "0.1.0",
    description = "HID Report descriptor compiler",
    author = "Nicolas Pouillon",
    author_email = "nipo@ssji.net",
    license = "BSD",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
    ],
    use_2to3 = False,
    packages = find_packages(),
)
