from setuptools import setup

setup(
    name='spolyrics',
    version='1.0.3',
    description='A minimalist, borderless, zero-delay synced lyrics miniplayer for Spotify on Windows.',
    author='SpoLyrics Team',
    py_modules=['main'],
    python_requires='>=3.8',
    install_requires=[
        'requests',
        'winsdk',
        'pillow'
    ],
    entry_points={
        'gui_scripts': [
            'spolyrics=main:start_app',
        ],
    },
)
