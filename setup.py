from setuptools import setup, find_packages


def readme():
	with open('README.md') as f:
		return f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()	

setup(
	name='log_analysis',
	version='1',
	python_requires='>=3.4',
	description="Log Analysis Project for Udacity's Full Stack Developer Course",
	long_description=readme(),
	# url='',
	author='Maxence',
	author_email='maxi730@gmail.com',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'logA = log_analysis.__main__:main'
		]
	},
	install_requires=[requirements]
)
