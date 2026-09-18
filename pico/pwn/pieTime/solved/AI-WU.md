**1.** Ketika membaca judul soal, saya menduga "pie" merujuk pada **Position Independent Executable (PIE)**. Ini merupakan mekanisme keamanan yang membuat program dimuat ke alamat memori dasar (*base address*) yang berbeda dan acak setiap kali dijalankan (ASLR). 

**2.** Karena diberikan *source code*, hal pertama yang saya lakukan adalah menganalisisnya. Di sini kita dapat melihat 3 buah *function* di dalam program: `main` (fungsi utama), `win`, dan sebuah *segfault handler*. Fungsi `win` adalah fungsi yang akan mencetak isi dari flag ke terminal, sementara fungsi *segfault handler* akan otomatis berjalan ketika input alamat memori yang diberikan oleh *player* tidak valid (menyebabkan *segmentation fault*).

**3.** Fokus utama kita adalah *function* `win`. *Function* ini merupakan kunci kemenangan karena akan mencetak flag yang disembunyikan. Dengan kata lain, tugas kita adalah memanipulasi alur program agar mengeksekusi `win()`.

**4.** Menganalisis *function* `main`, terdapat baris yang meminta input dari *player* berupa *string* (yang merepresentasikan alamat memori). Input tersebut kemudian dikonversi menjadi sebuah *function pointer*. *Function pointer* sendiri merupakan variabel yang menyimpan alamat memori dari sebuah instruksi kode. Di baris pemanggilan fungsi (misalnya `foo();`), program melakukan instruksi `CALL` ke alamat memori yang kita berikan tadi. Pada detik ini, alamat yang *player* ketikkan akan dimuat ke dalam register **RIP (Instruction Pointer)**.

**5.** Seperti yang kita tahu, RIP merupakan register yang berperan sebagai penunjuk jalan bagi CPU untuk menentukan instruksi mana yang harus di- *fetch* dan dieksekusi selanjutnya. Karena kita memegang kendali atas eksekusi melalui *function pointer* tersebut, kita tinggal memberikan alamat memori dari *function* `win` agar RIP melompat ke sana.

**6.** Namun, di sinilah tantangannya. Karena **PIE aktif**, alamat absolut dari `win()` selalu berubah. Untungnya, sebelum eksekusi input, program memberikan *information leak* berupa alamat asli dari *function* `main` pada saat *runtime* (saat program sedang berjalan). Kita harus menyimpan alamat ini karena ini adalah kunci untuk mengalahkan PIE.

**7.** Di sini kita menggunakan bantuan alat analisis seperti GDB (dengan Pwndbg) atau sekadar perintah `objdump`/`readelf` untuk melihat struktur *binary*-nya. Tujuan kita bukan mencari alamat statis untuk di-*hardcode*, melainkan mencari **Offset**. *Offset* adalah jarak relatif antara sebuah fungsi dengan awal program (atau *Base Address*), dan nilai *offset* ini **tidak pernah berubah** meskipun PIE aktif.

**8.** Instruksi yang kita jalankan di GDB (misalnya dengan `print win` dan `print main`) akan mencetak alamat *virtual* saat di-*debug*. Dari sini, kita bisa menghitung jarak (*offset*) antara fungsi `main` dan fungsi `win`. Atau lebih mudahnya, kita bisa melihat *offset* asli mereka di dalam file *binary* langsung. 
Misalnya:
* Offset dari `main` = `0x11b9`
* Offset dari `win`  = `0x12a7`

**9.** Dengan berbekal *Information Leak* (Alamat `main` yang bocor saat *runtime*) dan *Offset*, kita bisa menghitung alamat `win` yang sebenarnya pada sesi tersebut dengan rumus matematika sederhana:
`Base Address = Leaked Address of main - Offset main`
`Real Address of win = Base Address + Offset win`

**10.** Terakhir, saya membuat *exploit script* (biasanya menggunakan Python dengan *library* `pwntools`) untuk mengotomatisasi proses ini. *Script* akan menangkap alamat `main` yang bocor, melakukan kalkulasi di atas untuk mendapatkan alamat `win` yang valid, lalu mengirimkannya kembali ke program. Program akan menerima alamat tersebut, memasukkannya ke *function pointer*, dan BOOM! Program melompat ke fungsi `win()` dan mencetak *flag*.