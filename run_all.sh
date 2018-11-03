#!/usr/bin/env bash

./src/align_times.py data/t1_pps.bin data/t2_pps.bin data/tiempos.bin data/t1_pps_aligned.bin data/t2_pps_aligned.bin data/tiempos_aligned.bin
./src/estimate_phi.py data/tiempos_aligned.bin data/sic_phi.bin
./src/real_phi.py data/t1_pps_aligned.bin data/t2_pps_aligned.bin data/real_phi.bin
./src/calc_mtie.py data/real_phi.bin data/sic_phi.bin data/t1_pps_aligned.bin

