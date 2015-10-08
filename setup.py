from distutils.core import setup

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
    packages = ["hrdc", "hrdc.descriptor",
                "hrdc.stream", "hrdc.stream.formatter",
                "hrdc.stream.optimizer", "hrdc.stream.parser",
                "hrdc.usage", "hrdc.util"],
)
