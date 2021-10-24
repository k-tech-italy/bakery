## K-Tech bakery

1. Make sure you have the following tools in your system:

    * cookiecutter (installed globally. eg. with pipx)
    * pyenv (for the target version required by the recipe see .python-project)
    * poetry (for the target version required by the recipe see .python-project)
    * npm (if needed. for the target version required by the recipe see .nvmrc)

    otherwise `make` will complain and exit.

2. Run:

    ```bash
    make bake
    ```
    will list the available cookies with the command to bake them

    **Warning:** Baking again a project will delete any changes you
    may have done in the corresponding demo folder
   
3. Bake the specific recipe as suggested by `make bake`
