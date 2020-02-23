using Statistics
using Plots

ppal_dir = pwd()

function init_lattice(L, N, l)

    FCWS = []

    grid = zeros((L, L))
    
    idx = 0

    while idx < N

        x_head = rand(1 : (L - 1))

        x_tail = x_head + l - 1

        row = rand(1 : L)

        positions = [(row, mod(j, 1 : L)) for j in x_head : x_tail]

        validator = true

        #Check if any of these positions have been taken
        for pos in positions

            if grid[positions[1][1], positions[1][2]] == 1

                validator = false
                
            end

        end

        #if any position has been taken don't do anything
        if validator == false
            #DO nothing

        #If all the positions are free then take it
        else
            
            idx += 1

            for j in x_head : x_tail

                grid[row, mod(j, 1 : L)] = 1
                
            end

            append!(FCWS, [positions])

        end
    end

    return FCWS, grid

end


function move_walkers(L, N, l, FCWS, grid)

    N_mov = 0

    k = 0
    
    @fastmath @inbounds for fcw in FCWS

        k += 1
        
        new_pos = [(0, 0) for j in 1 : l]

        #Choose 1 free nearest neighbours poisition
        i = fcw[1][1]
        j = fcw[1][2]

        lattice_pos = [(i, mod(j+1, 1:L)), (i, mod(j-1, 1:L)), (mod(i+1, 1:L), j), (mod(i-1, 1:L), j)]
        
        free_pos = []

        for pos in lattice_pos
            
            if grid[convert(Int32, pos[1]), convert(Int32, pos[2])] == 0
                
                append!(free_pos, [pos])
                
            end
        end
        

        #Only move if not occupied
        if length(free_pos) != 0
            
            #Move the head to the chosen position
            move_to = free_pos[rand(1:length(free_pos))]

            N_mov += 1
            
            #Update lattice for the tail
            grid[fcw[end][1], fcw[end][2]] = 0

            #Move the other particles following the head
            for i in 2 : l

                new_pos[i] = fcw[i-1]
                    
            end
            
            #Move the head
            new_pos[1] = move_to
            
            #Update FCW position
            FCWS[k] = new_pos
       
            #Update lattice for head
            grid[move_to[1], move_to[2]] = 1
                    
        end
    end
    
    mob = N_mov / N
    
    return mob, grid, FCWS
        
end

function simulate(L, N, l, t)

    FCWS, grid = init_lattice(L, N, l)
    
    heatmap(grid)

    mobility_arr = zeros(t)

    for k in 1 : t

        percentage = round(k/t * 100, digits=2)
        
        #println(percentage, " %", " done")

        mobility, grid, FCWS = move_walkers(L, N, l, FCWS, grid)
        
        @inbounds mobility_arr[k] = mobility
            
    end

    return mobility_arr, grid
        
end

function single_density(L, N, l, t, folder="Data")

    t0 = time_ns() #Start simulation

    mobility, grid = simulate(L, N, l, t)

    tf = time_ns() #Simulation finished

    ET = round((tf - t0) * 1e-9, sigdigits=3) #Compute elapsed time
    
    #Create folder if doesn't exist
    if ! isdir(folder)
        mkdir(folder)
    end
    
    #Choose folder
    cd(folder)
    
    #Write parameters used to file
    f_parameters = open("parameters_used.txt", "w")
    
    println(f_parameters, "L: ", L)
    println(f_parameters, "l: ", l)
    println(f_parameters, "N: ", N)
    println(f_parameters, "t: ", t)
    
    println(f_parameters, "\nElapsed time: ", ET)
    
    close(f_parameters)
    
    cd(ppal_dir) #Return to home directory
    
    println("Elapsed time: ", ET, " s")
    
    return mobility, grid

end

function several_densities(L, l, t, eq_t, times, densities, folder="Data")

    t0 = time_ns()

    k = 0
    
    if ! isdir(folder)
        mkdir(folder)
    end
    
    cd(folder)
    
    f = open("mobility.txt", "w")
    
    println(f, "#<M(t)>\tρ")
    println("#mobility\tdensity")
    
    #Simulate and compute mobility for each density
    for density in densities

        k += 1

        N = convert(Int, round(L^2 * density / l, digits=0))
        
        mean_mob = 0.
        
        #Average over "times" realisations
        for i in 1 : times
    
            mobility, grid = simulate(L, N, l, t)

            mean_mob += mean(mobility[eq_t : end])
            
        end
        
        mean_mob = mean_mob / times
        
        println(f, mean_mob, "\t", density)
        println(mean_mob, "\t", density)

    end
    
    close(f)
    
    tf = time_ns()
    
    ET = round((tf - t0) * 1e-9, sigdigits=3)
    
    f_parameters = open("parameters_used.txt", "w")
    
    println(f_parameters, "L: ", L)
    println(f_parameters, "l: ", l)
    println(f_parameters, "t: ", t)
    println(f_parameters, "Eq_t: ", eq_t)
    println(f_parameters, "times: ", times)
    
    println(f_parameters, "\nElapsed time: ", ET)
    
    close(f_parameters)
    
    cd(ppal_dir)

    println("Elapsed time: ", ET, " s")
    
end

L = 100
l = 1

t = 10^4
eq_t = 10^3

times = 5

densities = collect(0.01: 0.01 : 0.8)

foldername = "l_$l"

several_densities(L, l, t, eq_t, times, densities, foldername)
