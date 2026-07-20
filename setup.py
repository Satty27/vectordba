from setuptools import setup, Extension
from Cython.Build import cythonize

# Define a list of separate modules, each mapping to its own file
extensions = [
    Extension(
        "vectordba.premium.agents",
        ["src/vectordba/premium/agents.py"],
        define_macros=[("Py_LIMITED_API", "0x03080000")],
        py_limited_api=True
    ),
    Extension(
        "vectordba.premium.agent_persona",
        ["src/vectordba/premium/agent_persona.py"],
        define_macros=[("Py_LIMITED_API", "0x03080000")],
        py_limited_api=True
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': "3"}
    ),
    options={
            "bdist_wheel": {
                "py_limited_api": "cp38"  # Forces the final file tag output
            }
        }
)