def get_averages_per_station(lists_from_query, omitted_values=[]):
    averages = []
    for arr in lists_from_query:
        summed = 0
        count = 0
        for l in arr:
            if l not in omitted_values:
                summed += 1
                print(summed)
                count += l[0]
        if count != 0:
            averages.append(summed / count)
        else:
            averages.append(0)
    return averages
