# FCW model

Python library and Julia scripts to simulate several Flexible Chain Walker (FCW) models.

The python library can be useful to perform simulations for a single density and plot animations. To reproduce the results in reference <sup>1</sup>, which involve simulations for several densities, python is not efficient. For this purpose the model has been implemented also in Julia, which is a fast compiled programming language.

# Overview

The flexible chainlike walker (FCW) model was presented in 2008 by Takashi Mashiko, from the department of Mechanical Engineering of Shizuoka University. The model is proposed as a minimal model of a deformable moving object and as an extension of the regular random-walk model. In reference <sup>1</sup> the collective behaviour of a many-body system of FCW's is studied through numerical simulations on a square lattice. The results show that the FCW's exhibit a novelty type of irreversible aggregation, despite the lack of adherence in the model, which had always been assumed in all previous aggregation models. This irreversible aggregation without adherence proves to be an outcome of the deformability of the FCW's. Moreover, other FCW models were presented also by Takashi Mashiko in 2009 <sup>2</sup> and are also reviewed and studied here. These are the smart and the double-headed FCW models. It will be shown that providing the FCW's with some kind of intelligence isn't sufficient to avoid the irreversible aggregation while providing them with two heads is a sufficient condition to remove it.

More detailed information about the models can be found at the references given and in the [Review_FCW_models](https://github.com/agimenezromero/FCW-model/blob/master/Review_FCW_models.pdf) pdf file.

Table of contents
=================

<!--ts-->
   * [Overview](#overview)
   * [Table of contents](#table-of-contents)
   * [Requeriments](#requeriments)
   * [Documentation](#documentation)
       - [Python library](#python-library)
            - [Initialisation](#initialisation)
            - [Running simulations](#running-simulations)
       - [Julia script](#julia-script)
   * [Examples](#examples)

   * [Authors](#authors)
   * [License](#license)
<!--te-->

# Requeriments

Python 3 installed with the following libraries
- NumPy
- Matplotlib

Julia 1.0.4 installed with the following libraries
- Statistics
- Plots

# Documentation

## Python library

### Initialisation

To initialise the available Python classes (`FCW_model`, `SFCW_model` and `DHFCW_model`) the following parameters must be passed in:

- `L` (int) - Lattice length.
- `l` (int) - FCW length (nº of particles that conform a FCW)
- `rho` (float) - Density of FCW's

### Running simulations

There are 2 ways to run simulations for each of the classes previously mentioned: `simulate(t, folder)`, `animate(t, save_anim)`

- `t` (int) - Number of time steps to simulate.
- `folder` : (string, optional) - Folder name to save output files. Default: None.
- `save_anim` : (boolean, optional) - Save the animation instead of displaying it. Default: False.

## Julia script

Two simulation functions have been implemented: `single_density(L, N, l, t, folder="Data")` and `several_densities(L, l, t, eq_t, times, densities, folder="Data")`

- `L` (int) - Lattice length.
- `N` (int) - Number of FCW's.
- `l` (int) - FCW length (nº of particles that conform a FCW).
- `t` (int) - Number of time steps to simulate.

- `eq_t` (int) - Number of time steps to equilibrate and start computing average mobility.
- `times` (int) - Number of times to simulate for each density point.
- `densities` (array) - Density points to simulate.

- `folder` (string, optional) - Folder name to save output files. Default: "Data".

Just execute the self.assembling_chains.jl file or the Jupyter notebook with the desired function activated.

# Examples

## Python simulation

```python
from FCW_library import FCW_model

L = 100
l = 8
rho = 0.5

t = 10**4

foldername = 'l_%i' % l

model = FCW_model(L, l, rho)

model.simulate(t, folder=foldername)
```

## Python animation

```python
from FCW_library import FCW_model

L = 100
l = 8
rho = 0.5

t = 10**4

model = FCW_model(L, l, rho)

model.animate(t)
```

## Julia simulation

To perform a simulation with Julia the Jupyter-Notebook file or the .jl script file can be used. The Julia script can be run in background so that multiple simulations can be thrown at once.

To run the Julia script in background just type the following command in the bash

```bash
nohup FCW_model.jl > outfile.out &
```

this will run the script in the background writting the print outputs in the outfile.out file. The "&" command will let the cmd window free.

# Authors
* **A. Giménez-Romero**

# License
This project is licensed under the GNU General Public License - see the [LICENSE.md](https://github.com/agimenezromero/FCW-model/blob/master/LICENSE) file for details

# References
1. [Takashi Mashiko. “Irreversible aggregation of flexible chainlike walkers without adherence”.In:Phys. Rev. E78 (1 July 2008), p. 011106.](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.78.011106)
2. [Takashi Mashiko. “Effect of Individual Properties of Flexible Chainlike Walkers in a Many-Body System”. In:The Open Transport Phenomena Journal1 (Oct. 2009), pp. 30–34.](https://benthamopen.com/ABSTRACT/TOTPJ-1-30)
