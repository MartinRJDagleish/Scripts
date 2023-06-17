import os
from datetime import date
from sys import argv


def export_orca_out_part(list, filename="Output"+date.today().strftime("%d_%m_%Y")):
    with open(filename, 'w', encoding="utf-8") as f:
        for item in list:
            f.write(f"{item}\n")
    return None

def orca_read_ir_spectrum(file,export_bool=False):
    #* -----------------------
    #* FILTERING co-routine
    #* -----------------------
    # ! Check if file exists:
    cwd = os.listdir()
    if file in cwd: 
        # ! filtering for IR SPECTRUM part in output
        with open(file,encoding="utf-8") as f:
            f_lines = [line.strip("\n") for line in f]
            spec_line_ind_start = f_lines.index("IR SPECTRUM")-1 # ! starts with "--------"
            
            stop_index_list = []

            #* WORKING V1
            for i, item in enumerate(f_lines[spec_line_ind_start:-1]):
                if len(stop_index_list) != 1:
                    if f_lines[spec_line_ind_start+i] == f_lines[spec_line_ind_start+i+1]: # ! tests for two empty lines
                        stop_index_list.append(i+spec_line_ind_start)
                else:
                    break 
            
            spec_line_ind_end = stop_index_list[0]
    else:
        raise FileNotFoundError("The requested file could not be found!")
    
    #* -----------------------
    #* EXPORTING co-routine
    #* -----------------------

    def export_option():
        export_bool_input = input("Do you want to export the IR-Part to a file? (Choose: 'Yes', 'No', 'True', 'False', 0, 1)\n\n")
        # export_bool_input = "True" #! for testing purpose 
        if export_bool_input in ["True", "Yes", "1"]:
            export_bool = True
        elif export_bool_input in ["False", "No", "0"]:
            export_bool = False
        return export_bool
    export_bool = export_option()

    if export_bool:
        global output_name 
        output_name = os.path.basename(file) + "_IR_Part.out"
        export_orca_out_part(f_lines[spec_line_ind_start:spec_line_ind_end], output_name)

    return f_lines[spec_line_ind_start:spec_line_ind_end]

def mapspc_option():
    export_bool_input = input("Do you want to have a .csv for the plot? (Choose: 'Yes', 'No', 'True', 'False', 0, 1)\n\n")
    # export_bool_input = "True" #! for testing purpose 
    if export_bool_input in ["True", "Yes", "1"]:
        export_bool = True
    elif export_bool_input in ["False", "No", "0"]:
        export_bool = False
    return export_bool

def orca_mapspc_from_ir(file):
    os.system(f"orca_mapspc {file} ir -w25")
    return None

if __name__=='__main__':
    file = argv[1]
    ir_part_lines = orca_read_ir_spectrum(file)
    print()
    print("------------------------------------------------------------------")
    for line in ir_part_lines:
        print(line+"\n")
    print("------------------------------------------------------------------")
    print()
    if mapspc_option():
        orca_mapspc_from_ir(output_name)