from distutils.core import setup

setup(
    name="Slowloris",
    py_modules=["slowloris"],
    entry_points={"console_scripts": ["slowloris=slowloris:main"]},
    version="0.0.45",
    description="Low bandwidth DoS tool. Slowloris rewrite in Python.",
    author="lpmb45",
    author_email="ludovic.marco.p@proton.me",
    url="https://github.com/MarcoPalomo/slow-hugo-loris"
    keywords=["dos", "http", "slowloris"],
    license="MIT",
)
