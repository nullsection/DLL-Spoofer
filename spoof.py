import pefile
import os 
import argparse

def get_exported_functions(dll_path):
    pe = pefile.PE(dll_path)
    exported_functions = []

    for entry in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        func_name = entry.name.decode('utf-8') if entry.name else f"Function_{entry.ordinal}"
        exported_functions.append(func_name)

    return exported_functions

def generate_cpp_file(dll_path, output_cpp_file, exported_functions, messagebox):
    with open(output_cpp_file, "w") as cpp_file:
        dll_no_ext = os.path.splitext(os.path.basename(dll_path))[0]
        cpp_file.write("// dllmain.cpp : Defines the entry point for the DLL application.\n")
        cpp_file.write("#include \"pch.h\"\n")
        cpp_file.write("#include <iostream>\n")
        cpp_file.write("#include <Windows.h>\n")
        cpp_file.write("#include <windows.h>\n\n")
        
        if not messagebox:
            for func_name in exported_functions:
                cpp_file.write(f'#pragma comment(linker, "/export{func_name}={dll_no_ext}.{func_name}")\n')
                cpp_file.write("\n")
        else:
            cpp_file.write("extern \"C\" {\n\n")
            for func_name in exported_functions:
                
                cpp_file.write(f"__declspec(dllexport) void {func_name}() {{\n")
                cpp_file.write(f'    MessageBox(NULL, L"{func_name} called", L"Function Call", MB_OK);\n')
                
                cpp_file.write("}\n\n")
            cpp_file.write("}\n\n")

        # DllMain function
        cpp_file.write("BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {\n")
        cpp_file.write("    switch (ul_reason_for_call) {\n")
        cpp_file.write("    case DLL_PROCESS_ATTACH:\n")
        #cpp_file.write(f"\t\t{exported_functions[0]}();\n")
        cpp_file.write("    case DLL_THREAD_ATTACH:\n")
        cpp_file.write("    case DLL_THREAD_DETACH:\n")
        cpp_file.write("    case DLL_PROCESS_DETACH:\n")
        cpp_file.write("        break;\n")
        cpp_file.write("    }\n")
        cpp_file.write("    return TRUE;\n")
        cpp_file.write("}\n")
        cpp_file.close()
        print("Saved Spoofed Template.")

def main():
    

    parser = argparse.ArgumentParser(description="Generate a C++ source file for a DLL that displays MessageBox for exported functions.")
    parser.add_argument("dll_path", help="Path to the DLL to inspect and create the C++ source for.")
    parser.add_argument("--messagebox",action="store_true",default=False, help="If set, MessageBoxA all exports instead of proxy")
    args = parser.parse_args()

    output_cpp_file = "ExportedFunctions.cpp"  # Output C++ source file

    exported_functions = get_exported_functions(args.dll_path)
    generate_cpp_file(args.dll_path, output_cpp_file, exported_functions, args.messagebox)

if __name__ == "__main__":
    main()
