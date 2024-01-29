from distutils.core import setup

setup(
    name='unbabel_cli',
    version='1.0',
    packages=['app'],
    entry_points={
        'console_scripts': [
            'unbabel_cli=app.unbabel_cli:main',
        ],
    },
)
