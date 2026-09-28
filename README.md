# FoldX PositionScan heatmap

A small script to visualize the results of a FoldX `PositionScan` run as a ΔΔG heatmap (positions x amino acid substitutions), similar to the figures
commonly used in alanine-scanning / interface mutagenesis papers.

## Background

FoldX's `PositionScan` command mutates a given residue to all 20 standard amino acids and reports the change in stability (ΔΔG) for each substitution.
This is useful for identifying residues that are important for protein stability or, when applied to residues at a binding interface, for identifying residues that may be important for the interaction between two chains (e.g. after first running `AnalyseComplex` to get the list of interface residues).

**Note:** `PositionScan` (like `BuildModel`) reports the change in overall stability of the structure you give it. If you ran it on a multi-chain complex, this reflects folding + binding effects combined, not binding energy in isolation. To isolate the binding contribution, you would need to run `AnalyseComplex` on the mutant structures FoldX generates and compare against the wild-type interaction energy. 

This script itself is agnostic to that distinction, it just visualizes whatever ΔΔG values are in the `PositionScan` output file.

## What the Python script does

- Parses a `..._scanning_output.txt` file produced by FoldX's `PositionScan`
- Filters to the 20 standard amino acid substitutions (drops FoldX's special markers, e.g. `e`, `o`)
- Ranks positions by ΔΔG (default: the Alanine-substitution value, which is a cleaner does-this-side-chain-matter signal than the raw maximum, since bulky substitutions like Trp/Tyr/Cys can dominate the max just from steric clashes)
- Plots a heatmap (positions x amino acids), with a diverging color scale centered at 0
- Optionally splits the plot into one panel per chain

## Requirements

pandas
matplotlib
Python 3.9+.

## Usage

```bash
python foldx_heatmap.py scanning_output.txt
```

## Input format

The script expects the raw `PositionScan` output file, with lines like:
```bash
PHEA64G 2.87647
PHEA64A 1.8766
...
```

Each line: 3-letter wild-type code + chain letter + residue number + 1-letter mutant code, tab-separated from the ΔΔG value.

## Output

A PNG heatmap (default: `heatmap_position_scan.png`), plus a summary printed to the terminal showing which positions were selected and their ΔΔG values.

## Caveats

- FoldX does not always generate all 20 substitutions for every position (e.g. a missing His or a non-standard residue code); missing values show up as blank cells in the heatmap rather than being interpolated.
- The default color scale (e.g. `--vmin -3 --vmax 8`) may need adjusting depending on the range of your own ΔΔG values.
- Ranking by `max` can surface positions where the "importance" is really an artifact of steric clash from a bulky substitution rather than loss of a genuine interaction. Ranking by alanine is generally a more reliable signal, but still an approximation, not a substitute for experimental validation.
