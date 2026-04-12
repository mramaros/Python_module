def ft_count_harvest_recursive():
    day = int(input("Days until harvest: "))

    def recursive(counter, total):
        if counter > total:
            return
        print("Day", counter)
        recursive(counter + 1, total)

    recursive(1, day)
    print("Harvest time!")
