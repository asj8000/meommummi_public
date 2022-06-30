
sim_msd(ratings, 'Dave','Alex')

def sim_msd(data, name1, name2):
    sum = 0
    count = 0
    for movies in data[name1]:
        if movies in data[name2]: #같은 영화를 봤다면
            sum += pow(data[name1][movies]- data[name2][movies], 2)
            count += 1

    return 1 / ( 1 + (sum / count) )