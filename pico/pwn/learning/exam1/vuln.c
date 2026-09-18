#include <stdio.h>

void verifikasi_kode() {
    char buffer[10]; // Kita memesan ruang (laci) sebanyak 10 karakter di Stack
    
    printf("Masukkan kode rahasia: ");
    
    // Fungsi ini akan mengambil ketikan dari keyboard
    // dan menyimpannya ke variabel 'buffer'
    gets(buffer); 
    
    printf("Kode divalidasi.\n");
}

int main() {
    verifikasi_kode();
    return 0;
}