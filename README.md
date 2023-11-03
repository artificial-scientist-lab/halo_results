## Instructions for repeating results from our paper

To repeat the inverse-design of the experimental setups, install the [pytheus package](https://github.com/artificial-scientist-lab/PyTheus)
```
pip install pytheusQ
```
### 4-dimensional 4-particle GHZ state
Run
```
pytheus run 4d4pGHZ.json
```
A directory `output` is created were results are stored.

The parameters of the computation can be changed in `4d4pGHZ.json`


### Non-local creation of a 4-dimensional Bell state
Run
```
pytheus run nonlocal4dBell.json
```
A directory `output` is created were results are stored.

The parameters of the computation can be changed in `nonlocal4dBell.json`

### Plotting an experimental setup

Copy the `graph` dictionary found in a `clean` result and paste into `plotscript.py`.

This automatically produces two files `path_identity.png` and `bulk_optics_path_encoding.png`.These are first drafts for the final experiment. For instructions for how to translate the graph result by hand or adjust the automatically translated setup, refer to our [accompanying paper]( 	
https://doi.org/10.48550/arXiv.2210.09980).

