from setuptools import setup

setup(
    name='spolyrics',
    version='1.3.4',
    description='A minimalist, borderless, zero-delay synced lyrics miniplayer for Spotify on Windows.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='SpoLyrics Team',
    packages=['spolyrics'],
    entry_points={
        'gui_scripts': [
            'spolyrics=spolyrics.__main__:start_app',
        ],
    },
    python_requires='>=3.8',
    install_requires=[
        'winsdk',
        'requests',
        'pystray',
        'pillow'
    ],
)
