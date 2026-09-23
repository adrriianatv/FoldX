## Prepare every item needed

> [!IMPORTANT]
> This explanation is in Powershell commands!!

Before doing anything, **every** item needed for this process should be in the same working directory. This includes the FoldX program file (.exe) and the .pdb to which the process is gonna happen. 

To simplify, change the foldx .exe to a shorter version. 

```powershell
Rename-Item foldx_1_20270131.exe foldx.exe
```

## Repair the structure .pdb

This command cleans up a structure before you analyze it, by rearranging side chains that have steric clashes, bad torsion angles or unusually high energy, so the whole structure sits at a lower energy. It's like smoothing out a crumpled shirt before measuring it, since the wrinkles would otherwise distort every number you take.

```powershell
.\foldx --command=RepairPDB --pdb=your-protein.pdb
```

⚫ Output `your-protein_Repair.pdb` and `yourprotein_Repair.fxout`

> [!NOTE]
> An .fxout file is a plain-text output file. It contains the numerical results of energy calculations, including free energy changes (ΔΔ G), Van der Waals forces and hydrogen bonds. You can easily open and read it using any standard text editor (like Notepad or VS Code) or import it into Python or R for data analysis.

## Analyse complex

This command measures **how strongly two or more chains in a complex bind each other**, reporting the interaction energy (more negative means tighter binding), the residues at the interface with their contributions (H-bonds, van der Waals, electrostatics, solvation) and the buried surface area.

```powershell
.\foldx --command=AnalyseComplex --pdb=ug22_dimer_Repair.pdb --analyseComplexChains=A,B
```
## Position scan

Something to take into account is that running `PositionScan` after `AnalyseComplex`, using the list of interacting amino acids, will get you the **global** change in stability ($\Delta G_{fold}$) of the protein complex, not the binding energy between monomers ($\Delta G_{bind}$). If your PDB is a complex between monomers, `PositionScan` will evaluate how the mutation affects the total stability of the complex. Even if this includes indirectly the interactions in the interface, it does not isolate the specific impact to the binding strength. 

> [!TIP]
> The list that is given to you by `AnalyseComplex` does not specify to which amino acid are you going to do the mutations. As specified in the user guide:
> - a 20 amino acids
> - d 24 amino acids (Includes phosphorylated Tyr, Ser and Thr and hydroxyl Proline)
> - h {"GLY", "ALA", "LEU", "VAL", "ILE","THR", "SER", "CYS", "MET", "LYS", "TRP", "TYR", "PHE", "HIS"}
> - c {"ARG", "LYS", "GLU", "ASP", "HIS"} p {"ARG", "LYS", "GLU", "ASP", "HIS", "TRP", "TYR","THR", "SER", "GLN", "ASN"}
> - n......4 bases, it mutates any base to the other three and itself.
> - or any amino acid in one letter-code, i.e. LC43G

```powershell
.\foldx.exe --command=PositionScan --pdb=ug22_tetramer_letras_Repair.pdb --positions=KA101a,IA104a,SA105a,AA107a,YA108a,EA133a,SA204a,LA207a,RA208a,SA209a,FA211a,NA212a,EA225a,SC58a,QC461a,YC462a,WC465a,RC468a,KC484a,LC485a,MC487a,QC488a,EC491a,VC492a,KC514a
```

