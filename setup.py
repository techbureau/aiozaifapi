import io
import re
from setuptools import setup, find_packages


with io.open('README.md', encoding='utf-8') as fp:
    readme = fp.read()

with io.open('aiozaifapi/__init__.py', encoding='utf-8') as fp:
    version = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

setup(
    name='aiozaifapi',
    version=version,
    description='Zaif API Client with asyncio',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/techbureau/aiozaifapi',
    author='Hideo Hattori',
    author_email='hattori@techbureau.jp',
    packages=find_packages(),
    license='MIT',
    keywords='zaif asyncio api',
    classifiers=[
      'Development Status :: 4 - Beta',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License'
    ],
    install_requires=['aiohttp', 'async_timeout', 'zaifapi']
)
