from setuptools import setup

setup(
    name='spolyrics',
    version='1.2.0',
    description='A minimalist, borderless, zero-delay synced lyrics miniplayer for Spotify on Windows.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='SpoLyrics Team',
    py_modules=['main', 'assets'],
    python_requires='>=3.8',
    install_requires=[
        'winsdk',
        'requests',
        'pystray',
        'pillow'
    ],
    entry_points={
        'gui_scripts': [
            'spolyrics=main:start_app',
        ],
    },
)
