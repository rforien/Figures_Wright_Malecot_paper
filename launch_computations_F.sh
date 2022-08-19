#!/bin/bash
#SBATCH -J computationWrightMalecot
#SBATCH -o sorties_WM.out
#SBATCH -e error_WM.out
#SBATCH --ntasks=7
#SBATCH --cpus-per-task=1
#SBATCH -N 1

#SBATCH --mail-type=ALL

#SBATCH --mail-user=raphael.forien@inrae.fr

ml python/3.9.0

d=(2 2 2 3 3 3 3)
alpha=(1.5 1.5 2 1.5 1.5 2 2)
beta=(1.5 2.5 2.5 2.5 3.5 2.5 3.5)

out_dir="${HOME}/WrightMalecot/out"

echo $out_dir

srun -N1 -n1 ./test.py &

for i in ${!d[@]}
do
#	srun -p pcbiom2x ./compute_F.py -d "${d[$i]}" --alpha "${alpha[$i]}" --beta "${beta[$i]}" --output ${out_dir}/F_values_run_${i} &
	echo $i
done


