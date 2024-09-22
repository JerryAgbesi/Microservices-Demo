package main

import (
	"log"

	"github.com/jerryAgbesi/microservices-demo/showtimes/pkg/models/mongodb"
)

type application struct {
	errorLog  *log.Logger
	infoLog   *log.Logger
	showtimes *mongodb.ShowTimeCollection
}

func main() {
	// infoLog := log.New(os.Stdout, "INFO\t", log.Ldate|log.Ltime)
	// errLog := log.New(os.Stderr, "ERROR\t", log.Ldate|log.Ltime|log.Lshortfile)

}
