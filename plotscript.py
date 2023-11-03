import graphplot as gp
import pytheus

graphdict = {
        "(0, 3, 2, 0)": 1.0,
        "(0, 5, 1, 0)": 1.0,
        "(1, 3, 1, 0)": 1.0,
        "(1, 5, 2, 0)": 1.0,
        "(3, 5, 0, 0)": 1.0,
        "(0, 4, 0, 0)": 1.0,
        "(1, 4, 3, 0)": 1.0,
        "(0, 2, 3, 0)": 1.0,
        "(2, 4, 0, 0)": 1.0,
        "(1, 2, 0, 0)": 1.0
    }

graph = pytheus.fancy_classes.Graph(graphdict)

gp.PlotPathIdentity(graph, filename = "path_identity")
gp.PlotBulkOpticsPathEncoding(graph, filename = "bulk_optics_path_encoding")