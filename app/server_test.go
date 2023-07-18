package main

import (
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestAction(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/action", nil)
	w := httptest.NewRecorder()
	getAction(w, req)
	res := w.Result()
	defer res.Body.Close()
	data, err := ioutil.ReadAll(res.Body)
	if err != nil {
		t.Errorf("expected error to be nil got %v", err)
	}
	if string(data) != "Action Request HTTP!\n" {
		t.Errorf("expected 'Action Request HTTP!' got %v", string(data))
	}
}

func TestRoot(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	w := httptest.NewRecorder()
	getRoot(w, req)
	res := w.Result()
	defer res.Body.Close()
	data, err := ioutil.ReadAll(res.Body)
	if err != nil {
		t.Errorf("expected error to be nil got %v", err)
	}
	if string(data) != "Welcome\n" {
		t.Errorf("expected 'Action Request HTTP!' got %v", string(data))
	}
}
