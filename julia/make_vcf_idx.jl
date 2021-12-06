using GZip
function make_vcf_idx(file, outfile)
	if occursin(".gz", file)
		GZip.open(file) do f
			controld=Dict()
			for line in eachline(f)
				if string(line[1]) != "#"
					line_array=split(line,"\t")
					chromosome=replace(line_array[1],"chr"=>"")
					if !haskey(controld,chromosome) 
						controld[chromosome]=[line_array[2]]
					else
						push!(controld[chromosome],line_array[2])
					end
				end
			end
			for key in keys(controld)
				open(outfile, "a") do f
					write(f, string(key,","))
				end
				counter =0
				for item in controld[key]
					counter += 1
					if counter < length(controld[key])
						open(outfile, "a") do f
							write(f, string(item,","))
						end
					else 
						open(outfile, "a") do f
							write(f, string(item,"\n"))
						end
					end
				end
			end
		end
	else
		open(file) do f
			controld=Dict()
			for line in eachline(f)
				if string(line[1]) != "#"
					line_array=split(line,"\t")
					chromosome=replace(line_array[1],"chr"=>"")
					if !haskey(controld,chromosome) 
						controld[chromosome]=[line_array[2]]
					else
						push!(controld[chromosome],line_array[2])
					end
				end
			end
			return controld
			for key in keys(controld)
				open(outfile, "a") do f
					write(f, string(key,","))
				end
				counter =0
				for item in controld[key]
					counter += 1
					if counter < length(controld[key])
						open(outfile, "a") do f
							write(f, string(item,","))
						end
					else 
						open(outfile, "a") do f
							write(f, string(item,"\n"))
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
@timeit to "file2 parse" make_vcf_idx(ARGS[1],ARGS[2])
println(to)

open(file2) do f
	controld=Dict()
	for line in eachline(f)
		if string(line[1]) != "#"
			line_array=split(line,"\t")
			chromosome=replace(line_array[1],"chr"=>"")
			if !haskey(controld,chromosome) 
				controld[chromosome]=[line_array[2]]
			else
				push!(controld[chromosome],line_array[2])
			end
		end
	end
	return controld
end




