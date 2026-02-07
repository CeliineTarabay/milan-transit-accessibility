# milan-transit-accessibility

A small experiment in transit accessibility for Milan.

Starting from a fixed origin, the project computes travel times on a regular grid using GTFS and OSM data. The analysis is repeated under different transfer constraints to observe how accessibility changes when transfers are limited.

## What this shows
- How far you can reach from a single origin within fixed travel times
- How transfer limits reshape accessibility patterns
- Why single-line journeys often feel shorter than multi-transfer ones, even when total time is similar

## Data
- GTFS: ATM Milan
- OSM: OpenStreetMap (street network)

## Method
- Build a regular grid over the Milan area
- Compute travel times from one origin using public transport + walking
- Repeat the computation with different transfer limits
- Export results as grid layers for visualization in QGIS

## Output
- Grid-based travel time layers (minutes)
- Transfer-constrained accessibility maps

## Tools
- Python
- r5py
- QGIS (for visualization)

## Notes
This is an exploratory project. The goal is understanding how network structure and transfers shape everyday accessibility.

