from setuptools import setup

setup(
    name='payment_engine',
    packages=[
        'payment_engine',
        'payment_engine.core'
    ],
    include_package_data=True,
    install_requires=[
        '',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)



