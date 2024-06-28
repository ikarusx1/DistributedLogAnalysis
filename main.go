package main

import (
	"log"
	"os"

	"github.com/joho/godotenv"
	"yourproject/loganalysis/logaggregator"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	aggregator := logaggregator.NewLogAggregator(
		os.Getenv("LOG_SOURCE_DIR"),
		os.Getenv("AGGREGATED_LOG_DIR"),
	)

	err = aggregator.AggregateLogs()
	if err != nil {
		log.Fatalf("Failed to aggregate logs: %v", err)
	}
}