import re
import pandas as pd

path = "yourprotein_Repair_scanning_output.txt"

# Pattern: 3 characters (WT) + chain letter (A or B) + number + letter (mutant) + tab + number
patron = re.compile(r'^([A-Za-z0-9]{3})([AB])(\d+)([A-Za-z])\t([-\d.eE+]+)$')

filas = []
with open(path) as f:
    for linea in f:
        linea = linea.strip()
        if not linea:
            continue
        m = patron.match(linea)
        if not m:
            print("No coincide:", linea)  # flag any unexpected line format
            continue
        wt3, cadena, pos, mut, ddg = m.groups()
        filas.append({"wt3": wt3, "cadena": cadena, "pos": int(pos), "mut": mut, "ddG": float(ddg)})

df = pd.DataFrame(filas)
print(df.shape) # Unlike the len() method, which only returns the number of rows, shape provides both row and column counts, making it a more informative method for understanding dataset size.
print(df.head(25)) # only prints in therminal de first 25 results to not overload it

aa_orden = ["G","A","L","V","I","P","R","T","S","C","M","K","E","Q","D","N","W","Y","F","H"]

# Keep only substitutions to the 20 standard amino acids (drop 'e', 'o', etc.)
df = df[df["mut"].isin(aa_orden)].copy()

# If a position-mutation pair appears twice (the WT reference row), keep the last one (the recalculated energy)
df = df.drop_duplicates(subset=["cadena", "pos", "mut"], keep="last")

print(df.shape)
print(df.head(25))

# Map 3-letter amino acid codes to 1-letter codes
three_to_one = {
    "ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLN":"Q","GLU":"E",
    "GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F",
    "PRO":"P","SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V","H1S":"H"
}
df["wt1"] = df["wt3"].map(three_to_one)

# Check if any wt3 code failed to map (would show up as NaN)
print(df[df["wt1"].isna()]["wt3"].unique())

# Build a readable row label, e.g. "F64 (A)"
df["etiqueta"] = df["wt1"] + df["pos"].astype(str) + " (" + df["cadena"] + ")"

print(df.head(10))

# For each position, find its highest ddG across all substitutions
# (candidates for hot spots, since a high value in any mutation is notable)
resumen = df.groupby("etiqueta")["ddG"].max().sort_values(ascending=False)
top = resumen.head(15).index.tolist()

print(resumen.head(15))

# For each position, look specifically at the substitution to Alanine
# (a cleaner signal for "important side chain", since Ala removes it
# without introducing steric clashes from a bulkier residue)
ala = df[df["mut"] == "A"].set_index("etiqueta")["ddG"].sort_values(ascending=False)
top_ala = ala.head(79).index.tolist()

print(ala.head(79))

top = top_ala

# Keep only the rows for our selected top positions
sub = df[df["etiqueta"].isin(top)]

# Pivot: one row per position, one column per amino acid, values = ddG
tabla = sub.pivot(index="etiqueta", columns="mut", values="ddG")

# Reorder rows to match our ranking, and columns to match the reference figure
tabla = tabla.reindex(index=top, columns=aa_orden)

top = top_ala

# Keep only the rows for our selected top positions
sub = df[df["etiqueta"].isin(top)]

# Pivot: one row per position, one column per amino acid, values = ddG
tabla = sub.pivot(index="etiqueta", columns="mut", values="ddG")

# Reorder rows to match our ranking, and columns to match the reference figure
tabla = tabla.reindex(index=top, columns=aa_orden)

print(tabla)

# Once the data is prepared, you call matplotlib to make the figure itself

import matplotlib.pyplot as plt

from matplotlib.colors import TwoSlopeNorm

vmin, vcenter, vmax = -3, 0, 8
norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)

# Split the table by chain, using the "(A)" / "(B)" suffix in the row labels
tabla_a = tabla[tabla.index.str.endswith("(A)")]
tabla_b = tabla[tabla.index.str.endswith("(B)")]

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(20, 0.5 * max(len(tabla_a), len(tabla_b)) + 2), sharey=False
)

im1 = ax1.imshow(tabla_a.values, cmap="bwr_r", norm=norm)
ax1.set_xticks(range(len(aa_orden)))
ax1.set_xticklabels(aa_orden)
ax1.set_yticks(range(len(tabla_a.index)))
ax1.set_yticklabels(tabla_a.index)
ax1.set_title("Chain A")

im2 = ax2.imshow(tabla_b.values, cmap="bwr_r", norm=norm)
ax2.set_xticks(range(len(aa_orden)))
ax2.set_xticklabels(aa_orden)
ax2.set_yticks(range(len(tabla_b.index)))
ax2.set_yticklabels(tabla_b.index)
ax2.set_title("Chain B")

fig.colorbar(im2, ax=[ax1, ax2], label="ddG (kcal/mol)")
plt.savefig("heatmap_position_scan_by_chain.png", dpi=200)
plt.show()
