from os import path
import pickle
from gig.performance import Performance
from writer.flukebox_writer import FlukeBoxWriter

def test_read_history_pickle():
    sample_path = path.join("data", "history", "2022-04-15 14-47-28 - Jazzge - Bova.pickle")
    with open(sample_path, "rb") as sample_pickle:
        perf = pickle.load(sample_pickle)
    FlukeBoxWriter().write(perf)
    

if __name__ == "__main__":
    test_read_history_pickle()
