1. ketika membaca judul saya, saya menduga pie mrujuk pada Positon independent executable/PIE. Ini merupkana mekanisme keamanan yang membuat program dimuat ke alamat memori yang berbeda dan acak setiap kali dijalankan.

2. Karena diberikan, hal pertama yang saya lakukan adalah menganalsis file source code. Di sini kita dapat melihat 3 buat function yang ada di dalam program, seperti main(fungsi utama), win, dan segfault handler. win adalah fungsi yang aman mencetak isi dari flag ke terminal sementara segfault adalah fungsi yang akan bekerja ketika input yang diberikan oleh player (dalam hal ini alamat memori) tidak valid, dia akan otomatis berjalan ketika segmentation fault terjadi.

3. Fokus utama kita adalah function win. Function ini merupakan kunci kemengangan karena akan mencetak flag yang disembunyikan nantinya. Dengan kata lain, tugas kita adalah membuat program mengeksekusi win(). 

4. Pertama kita perlu menganalisis kode utama atau function main terlebih dahulu, di sini kita memahami bahwa di dalam function main ada baris yang meminta inputan dari player berupa string dengan format alamat memori. Input tersebut nantinya akan dikonversi menjadi sebuah function pointer, function pointer sendiri merupakan jenis data yang menyimpan alamat memori dari sebuah instruksi kode (ex: alamat memori baris pertama functon win). Di baris foo();, program melakukan instruksi CALL ke alamat memori tadi. Pada detik ini, nilai yang player ketikan akan diterima mentah-mentah oleh register RIP. 

5. Seperti yang kita tahu, RIP merupakan register yang berperan sebagai mata bagi cpu untuk menunjukkan kode mana yang harus dieksekusi selanjutnya oleh IR (Instruction Register). Karena kita memegang kendali atas register RIP, kita tinggal mencari tahu alamat memori dari function win untuk dimasukkan ke program.

6. Sebelum eksekusi, kita mendapatkan information leak berupa  address of main atau alamat dari function main. Kita akan menyimpan alamat tersebut untuk digunankan nantinya.

7. Di sini kita perlu bantuan gdb untuk melakukan debug pada program. Ini berguna untuk menemukan alamat memori dari function win. Pertama kita akan menjalankan program nya, di sini kita mendapatkan address of main dan memasukkan address yang akan dijump oleh program.

8. Instruksi yang kita jalankan adalah print win, gdb akan mencetak alamat 