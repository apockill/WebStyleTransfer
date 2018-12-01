from setuptools import setup

setup(
    name='dataset_creation_crawler',
    scripts=["create_web_dataset.py"],
    version='0.1',
    description='',
    packages=['crawler'],
    install_requires=["selenium",
                      "tldextract"],
    zip_safe=False
)
