my_list = [1, 2, 3, 4, 5, 6]


for i, pkt in enumerate(my_list):
            print(i)
            if (6 == pkt): # checking if it the correct 
                print('correct packet')
                my_list= my_list[i+1:]
                
                break

print(my_list)