from django.conf import settings

def pick_file_list(pre_file):
    lis_file = []
    for f in pre_file:
        lis_file.append(f)
    #Reorder the list in a bidimensional list
    final_file = []
    while len(lis_file) != 0:
        first_file = lis_file[0]
        pip_id = first_file.pip_id
        lis_file.remove(first_file)
        for f in lis_file:
            if f.pip_id == pip_id:
                second_file = f
                lis_file.remove(f)
                break
        final_file.append([first_file, second_file, pip_id.pip_id])
    return final_file