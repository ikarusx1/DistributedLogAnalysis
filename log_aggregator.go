package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
)

type LogEntry struct {
	Timestamp int64  `json:"timestamp"`
	Level     string `json:"level"`
	Message   string `json:"message"`
}

type AggregatedData struct {
	Level   string
	Count   int
	Message string
}

func aggregateLogs(logEntries []LogEntry) map[string]*AggregatedData {
	aggregatedData := make(map[string]*AggregatedData)

	for _, entry := range logEntries {
		if _, ok := aggregatedData[entry.Level]; !ok {
			aggregatedData[entry.Level] = &AggregatedData{Level: entry.Level, Count: 0, Message: ""}
		}
		aggregatedData[entry.Level].Count++
	}
	return aggregatedData
}

func readLogs(filePath string) ([]LogEntry, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var logEntries []LogEntry
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		var entry LogEntry
		if err := json.Unmarshal(scanner.Bytes(), &entry); err != nil {
			log.Printf("Error unmarshalling log entry: %v", err)
			continue
		}
		logEntries = append(logEntries, entry)
	}

	return logEntries, scanner.Err()
}

func simulateDistributedAggregation(files []string) {
	var wg sync.WaitGroup

	for _, file := range files {
		wg.Add(1)
		go func(filePath string) {
			defer wg.Done()
			logEntries, err := readLogs(filePath)
			if err != nil {
				log.Printf("Error reading logs from %s: %v", filePath, err)
				return
			}

			aggregated := aggregateLogs(logEntries)
			for level, data := range aggregated {
				fmt.Printf("File: %s, Level: %s, Count: %d\n", filePath, level, data.Count)
			}
		}(file)
	}

	wg.Wait()
}

func main() {
	files := []string{"./server1.json", "./server2.json", "./server3.json"}
	simulateDistributedAggregation(files)
}