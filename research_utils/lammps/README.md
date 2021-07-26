# lammps module
## Image to Particles
```bash
  python research_utils/lammps/img2particle/Img2Particle.py research_utils/lammps/img2particle/256F_FS_Plane.PNG
```

## Tensile Test
```bash
  lmp_serial -in research_utils/lammps/in.tensiletest -v basedir research_utils/lammps r img2particle/256F_FS_Plane
```

