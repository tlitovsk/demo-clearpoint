package main

import (
	"io"
	"net/http"
)

func getAction(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Action Request HTTP!\n")
}

func getRoot(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Welcome\n")
}

func main() {
	http.HandleFunc("/", getRoot)
	http.HandleFunc("/action", getAction)
	http.ListenAndServe(":8080", nil)
}
