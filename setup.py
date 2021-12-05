from setuptools import setup, find_packages


setup(
    name="mkdocs-devicetree-plugin",
    version="0.0.1",
    description="MkDocs plugin for DeviceTree documentation",
    long_description="",
    include_package_data=True,
    package_data={"mkdocs_dt_plugin": ["templates/*.html"]},
    keywords="mkdocs",
    url="",
    author="Travis F. Collins",
    author_email="travis.collins@analog.com",
    license="EPL-2.0",
    python_requires=">=3.6",
    install_requires=["mkdocs>=1.0.4"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: EPL-2.0 License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": ["dt-plugin = mkdocs_dt_plugin.plugin:DeviceTreePlugin"]
    },
)
