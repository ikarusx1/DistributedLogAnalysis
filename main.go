package main

import (
	"log"
	"os"

	"github.com/joho/godotenv"
	"yourproject/loganalysis/logcollector"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	collector := logcollector.NewCollector(
		os.Getenv("SOURCE_DIRECTORY"),
		os.Getenv("DESTINATION_DIRECTORY"),
	)

	err = collector.CollectAndAggregateLogs()
	if err != nil {
		log.Fatalf("Failed to collect and aggregate logs: %v", err)
	}
}