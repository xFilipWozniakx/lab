package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Cześć! Twoja aplikacja w Go działa wewnątrz kontenera Docker! 🚀\n")
}

func main() {
	// Ustawiamy ścieżkę "/" oraz funkcję, która ma ją obsługiwać
	http.HandleFunc("/", handler)

	fmt.Println("Serwer wystartował na port 8080...")
	// Uruchamiamy serwer na porcie 8080
	http.ListenAndServe(":8080", nil)
}
