using GZip
function cd_maker(file2)
	if occursin(".gz", file2)
		GZip.open(file2) do f
			controld=Dict()
			for line in eachline(f)
				if string(line[1]) != "#"
					line_array=split(line,"\t")
					chromosome=replace(line_array[1],"chr"=>"")
					variant=line_array[4]*line_array[2]*line_array[5]
					if !haskey(controld,chromosome) 
						controld[chromosome]=[variant]
					else
						push!(controld[chromosome],variant)
					end
				end
			end
			return controld
		end
	elseif occursin(".eidx", file2)
		open(file2) do f
			controld=Dict()
			for line in eachline(f)
				if string(line[1]) != "#"
					line_array=split(line,",")
					chromosome=replace(line_array[1],"chr"=>"")
					variant=line_array[4]*line_array[2]*line_array[5]
					for variant in line_array[2:length(line_array)];
						if !haskey(controld,chromosome) 
							controld[chromosome]=[variant]
						else
							push!(controld[chromosome],variant)
						end
					end

				end
			end
			return controld
		end
	else 
		open(file2) do f
			controld=Dict()
			for line in eachline(f)
				if string(line[1]) != "#"
					line_array=split(line,"\t")
					chromosome=replace(line_array[1],"chr"=>"")
					variant=line_array[4]*line_array[2]*line_array[5]
					if !haskey(controld,string(chromosome)) 
						controld[string(chromosome)]=[variant]
					else
						push!(controld[string(chromosome)],variant)
					end
				end
			end
			return controld
		end
	end
end

function vcf_ann(file,controldict,outfile="out.vcf")
	controld=controldict
	if occursin(".gz", file)
		GZip.open(file) do f
			for line in eachline(f)
				if length(line) > 1
					if string(line[1]) != "#"
						line_array=split(line,"\t")
						chromosome=replace(line_array[1],"chr"=>"")
						variant=line_array[4]*line_array[2]*line_array[5]
						if !haskey(controld,chromosome) 
							open(outfile, "a") do output
								write(output, string(line,"\t\n"))
							end
						elseif (variant in controld[chromosome])
							open(outfile, "a") do output
								write(output, string(line,"\tX\n"))
							end
						else
							open(outfile, "a") do output
								write(output, string(line,"\t\n"))
							end
						end
					end
				end
			end
		end
	else
		open(file) do f
			for line in eachline(f)
				if length(line) > 1
					if string(line[1]) != "#"
						line_array=split(line,"\t")
						chromosome=replace(line_array[1],"chr"=>"")
						variant=line_array[4]*line_array[2]*line_array[5]
						if !haskey(controld,chromosome) 
							open(outfile, "a") do output
								write(output, string(line,"\t\n"))
							end
						elseif (variant in controld[chromosome])
							open(outfile, "a") do output
								write(output, string(line,"\tX\n"))
							end
						else
							open(outfile, "a") do output
								write(output, string(line,"\t\n"))
							end
						end
					end
				end
			end
		end
	end
end
using TimerOutputs
const to = TimerOutput()
println("Starting file 2")
@timeit to "file2 parse" controld=cd_maker(ARGS[2])
println("file 2 donezo! See stats below")
println(to)
println("Starting Annotation...")
@timeit to "annotate" vcf_ann(ARGS[1],controld,ARGS[3])
println("Fucking Right! Done!")
println(to)



