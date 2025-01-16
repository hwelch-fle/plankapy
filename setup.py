from setuptools import setup, find_packages

setup(
    name='plankapy',
    version='1.0.2',
    description='Python library for Planka API',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'plankapy': ['config/templates.json'],  # Include templates.json
    },
)
