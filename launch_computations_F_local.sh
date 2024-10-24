#!/bin/bash
#SBATCH -J computationWrightMalecot
#SBATCH -o sorties_WM.out
#SBATCH -e error_WM.out
#SBATCH --ntasks=7
#SBATCH --cpus-per-task= 2

#SBATCH --mail-type=ALL

#SBATCH --mail-user=raphael.forien@inrae.fr

# ml python/3.9

d=(2 3)
alpha=(1.5 1.5 2 2)
beta=(1.5 2.2 2.2 3)

out_dir="out2"

for i in ${!d[@]};
do
	for j in ${!alpha[@]};
	do
		./compute_F.py -d ${d[$i]} --alpha ${alpha[$j]} --beta ${beta[$j]} --output "${out_dir}/F_values_d-${d[$i]}_run-${j}"
	done
done


