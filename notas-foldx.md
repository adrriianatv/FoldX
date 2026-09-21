## Prepare every item needed

> [!IMPORTANT]
> This explanation is in Poweshell commands!!

Before doing anything, **every** item needed for this process should be in the same working directory. This includes the FoldX program file (.exe) and the .pdb to which the process is gonna happen. 

To simplify, change the foldx .exe to a shorter version. 

```
Rename-Item foldx_1_20270131.exe foldx.exe
```

## Repair the structure .pdb

The objective is to minimize the energy to avoid sterical clashes.

```
./foldx --command=RepairPDB --pdb=your-protein.pdb
```

Output `your-protein_Repair.pdb`
