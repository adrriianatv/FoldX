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
./foldx --command=RepairPDB --pdb=your-protein.pdb
```

⚫ Output `your-protein_Repair.pdb` and `yourprotein_Repair.fxout`

> [!NOTE]
> An .fxout file is a plain-text output file. It contains the numerical results of energy calculations, including free energy changes (ΔΔ G), Van der Waals forces and hydrogen bonds. You can easily open and read it using any standard text editor (like Notepad or VS Code) or import it into Python or R for data analysis.

## Analyse complex

This command measures **how strongly two or more chains in a complex bind each other**, reporting the interaction energy (more negative means tighter binding), the residues at the interface with their contributions (H-bonds, van der Waals, electrostatics, solvation), and the buried surface area.

```powershell
.\fold.exe --command=AnalyseComplex --pdb=ug22_dimer_Repair.pdb --analyseComplexChains=A,B
```
