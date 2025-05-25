import pefile

def get_exported_functions(dll_path):
    pe = pefile.PE(dll_path)
    exported_functions = []

    for entry in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        func_name = entry.name.decode('utf-8') if entry.name else f"Function_{entry.ordinal}"
        exported_functions.append(func_name)

    return exported_functions

def generate_rust_file(dll_path, output_rust_file, exported_functions):
    with open(output_rust_file, "w") as rust_file:
        rust_file.write("// Auto-generated Rust file for exported functions\n\n")
        
        for func_name in exported_functions:
            rust_file.write("#[no_mangle]\n")
            rust_file.write(f'pub extern "C" fn {func_name}() {{\n')
            rust_file.write(f"    main()\n")
            rust_file.write("}\n\n")

        print(f"Saved Rust exports file: {output_rust_file}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate a Rust file with pub extern functions from a DLL.")
    parser.add_argument("dll_path", help="Path to the DLL to inspect and create the Rust source for.")
    args = parser.parse_args()

    output_rust_file = "exports.rs"  # Output Rust source file

    exported_functions = get_exported_functions(args.dll_path)
    generate_rust_file(args.dll_path, output_rust_file, exported_functions)

if __name__ == "__main__":
    main()
