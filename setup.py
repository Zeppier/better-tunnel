from setuptools import setup

setup(
    name='better-tunnel',
    version='0.2',
    py_modules=['tunnel', 'Instance'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        better-tunnel=better-tunnel:cli
    '''
)
