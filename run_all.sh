#!/usr/bin/env bash


./src/align_pps.py data/t1_pps.bin data/t2_pps.bin data/t1_pps_aligned.bin data/t2_pps_aligned.bin
./src/estimate_phi.py data/tiempos.bin data/sic_phi.bin data/t1.bin
./src/real_phi.py data/t1_pps_aligned.bin data/t2_pps_aligned.bin data/real_phi.bin
./src/interp_real_phi.py data/t1_pps_aligned.bin data/real_phi.bin data/t1.bin data/real_phi_interp.bin
./src/calc_mtie.py data/real_phi_interp.bin data/sic_phi.bin data/t1.bin
