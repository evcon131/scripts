function line_counter(file)
	if occursin(".gz", file)
		GZip.open(file) do f
			line=0
			for i in eachline(f)
				if !occursin("#",i)
					line+=1
				end
			end
			return line
		end
	else
		open(file) do f
			line=0
			for i in eachline(f)
				if !occursin("#",i)
					line+=1
				end
			end
			return line
		end
	end
end
println(string(line_counter(ARGS[1]))," lines")






