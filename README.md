# boltzmann-tsp

Solves the traveling salesman problem with a boltzmann machine (neural network).
This is obviously not an optimal way to solve TSP, just a way to learn about boltzmann
machines!

Example Output:
```bash
$ python main.py

Distance Matrix
   [[ 0 10 20  5 18]
    [10  0 15 32 10]
    [20 15  0 25 16]
    [ 5 32 25  0 35]
    [18 10 16 35  0]]

Shortest paths (Distance=66):
    [0, 1, 4, 2, 3, 0]
    [0, 3, 2, 4, 1, 0]
    [1, 0, 3, 2, 4, 1]
    [1, 4, 2, 3, 0, 1]
    [2, 3, 0, 1, 4, 2]
    [2, 4, 1, 0, 3, 2]
    [3, 0, 1, 4, 2, 3]
    [3, 2, 4, 1, 0, 3]
    [4, 1, 0, 3, 2, 4]
    [4, 2, 3, 0, 1, 4]

Longest paths (Distance=120):
    [0, 2, 1, 3, 4, 0]

Running...
Temp:102613.36     PercentComplete:10.77 %     ETA:0:00:08    Flips:24695       BestDist:103     DeltaConsensus:-590.0     ValidStates:0/0
Temp:25495.16      PercentComplete:21.54 %     ETA:0:00:07    Flips:24712       BestDist:103     DeltaConsensus:-782.0     ValidStates:0/0
Temp:6496.91       PercentComplete:32.11 %     ETA:0:00:06    Flips:24274       BestDist:103     DeltaConsensus:460.0      ValidStates:0/0
Temp:1655.60       PercentComplete:42.68 %     ETA:0:00:05    Flips:24225       BestDist:103     DeltaConsensus:-302.0     ValidStates:0/0
Temp:432.71        PercentComplete:53.04 %     ETA:0:00:04    Flips:22422       BestDist:103     DeltaConsensus:-366.0     ValidStates:0/0
Temp:128.36        PercentComplete:62.40 %     ETA:0:00:03    Flips:16454       BestDist:101     DeltaConsensus:18.0       ValidStates:19/27
Temp:38.08         PercentComplete:71.65 %     ETA:0:00:02    Flips:10350       BestDist:85      DeltaConsensus:40.0       ValidStates:90/230
Temp:11.58         PercentComplete:80.42 %     ETA:0:00:01    Flips:3621        BestDist:66      DeltaConsensus:40.0       ValidStates:116/591
Temp:2.47          PercentComplete:90.37 %     ETA:0:00:00    Flips:198         BestDist:66      DeltaConsensus:155.0      ValidStates:116/651
Temp:0.48          PercentComplete:96.98 %     ETA:0:00:00    Flips:0           BestDist:66      DeltaConsensus:158.0      ValidStates:116/651
Boltzmann paths (Distance=66):
    [3, 2, 4, 1, 0, 3]

Score (out of 1, higher is better): 1.00
```
