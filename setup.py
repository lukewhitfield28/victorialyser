from setuptools import setup

setup(
   name="victorialyser",
   packages=["victorialyser"],
   package_data={"victorialyser": ["data.json", "main.ui"]},
   install_requires=["pillow", "PyQt6"],
   entry_points={
        'console_scripts': [
            'victorialyser = victorialyser:main',
        ]
    }
)
