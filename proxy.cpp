extern "C"
__declspec(dllexport)
__int64 <function>() {
    HMODULE h = LoadLibraryW(L"");
    if (!h) return 0;

    using InitFuncType = void* (WINAPI*)();  // Generic pointer return type

    InitFuncType realFunc = (InitFuncType)GetProcAddress(h, "<func>");
    if (!realFunc) return 0;

    void* result = realFunc();  // Call the real function

    return (__int64)result;  // Return its pointer value as an int64
}
